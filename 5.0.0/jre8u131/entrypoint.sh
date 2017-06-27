#!/bin/bash


AUTO_CONFIGURE=${AUTO_CONFIGURE:-1}
DEBUG_AUTO_CONFIGURE=${DEBUG_AUTO_CONFIGURE:-0}

POLL_INTERVAL=3
POLL_TIMEOUT=180


function configure() {

if [[ ! -d ${OPENDJ_HOME}/opendj/config ]]; then
	echo "OpenDJ Config Directory [${OPENDJ_HOME}/config] is missing, configuring..."

	echo "Running configuration."
	python2 ./setup.py
	if [[ ! $? -eq 0 ]]; then
		echo "Error setting up OpenDJ..."
		if [[ ${DEBUG_AUTO_CONFIGURE} -eq 0 ]]; then
			terminate 1
		else
			return 1
		fi
	fi
		echo "OpenDJ Configuration complete!"

fi

}

function configure_replication() {

if [[ ! -z "${DS_MASTER_HOST}" || ! -z "${DS_REPL_HOST_1}" || ! -z "${DS_REPL_HOST_2}" ]]; then

	echo "Running configuration for replication."
	python2 ./setup.py dsreplication
	if [[ ! $? -eq 0 ]]; then
		echo "Error setting up OpenDJ Replication..."
		if [[ ${DEBUG_AUTO_CONFIGURE} -eq 0 ]]; then
			terminate 1
		else
			return 1
		fi
	fi

	echo "OpenDJ Replication Configuration complete!"

	echo "Running initialization of replication."

	python2 ./setup.py dsreplication initialize

	if [[ ! $? -eq 0 ]]; then
		echo "Error initializing OpenDJ Replication..."
		if [[ ${DEBUG_AUTO_CONFIGURE} -eq 0 ]]; then
			terminate 1
		else
			return 1
		fi
	fi

	echo "OpenDJ Replication Initialization complete!"

fi

}


function check_status() {
	grep -q "Directory Server has started successfully" ${OPENDJ_HOME}/opendj/logs/server.out
	return $?
}


function poll() {

START_TIMESTAMP=$(date +%s)
TIMEOUT=$(expr ${START_TIMESTAMP} + ${POLL_TIMEOUT})

while true; do
	check_status
	if [[ $? -eq 0 ]]; then
		configure_replication
		break;
	else
		CURRENT_TIMESTAMP=$(date +%s)
		TIME_ELAPSED=$(expr ${CURRENT_TIMESTAMP} - ${START_TIMESTAMP})
		if [[ ${TIME_ELAPSED} -ge ${TIMEOUT} ]]; then
			echo "Exceeded poll timeout, exiting."
			terminate
			exit 1
		fi
		echo "[${TIME_ELAPSED} seconds] Polling for OpenDJ status... Sleeping for ${POLL_INTERVAL} seconds..."
		sleep ${POLL_INTERVAL}
	fi
done

}

function start(){
	if [[ ${AUTO_CONFIGURE} -eq 1 ]]; then
		echo "Autoconfiguration enabled..."
		configure
	else
		echo "Autoconfiguration disabled..."
	fi

	echo "Starting OpenDJ..."
	${OPENDJ_HOME}/opendj/bin/start-ds -N &
	export OPENDJ_PID=$!
	echo "OpenDJ started with PID ${OPENDJ_PID}..."

	if [[ ! -z "${DS_MASTER_HOST}" || ! -z "${DS_REPL_HOST_1}" || ! -z "${DS_REPL_HOST_2}" ]]; then
		poll
	fi

	wait ${OPENDJ_PID}
}

function terminate(){
	echo "Terminating Forgerock OpenDJ with PID ${OPENDJ_PID}..."
	kill ${OPENDJ_PID}
	echo "Terminated OpenDJ."
	exit ${1:-0}
}

if [[ "${1}" == "configure" ]]; then
	configure
	exit
elif [[ "${1}" == "configure_replication" ]]; then
	configure_replication
	exit
fi



trap terminate EXIT
start
