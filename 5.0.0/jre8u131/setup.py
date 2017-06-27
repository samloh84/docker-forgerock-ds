#!/usr/bin/env python2
import os
import socket
import subprocess
import sys
from collections import OrderedDict


def read_options(metadata):
    options = OrderedDict()
    for key, value in metadata.items():
        if isinstance(value, dict):
            type = value.get('type', 'string')
            default_value = value.get('default')
        else:
            type = 'string'
            default_value = None

        options[key] = os.getenv(key, default_value)
    return options


def build_args(options, metadata):
    args = []
    for key, value in metadata.items():
        if isinstance(value, dict):
            flag = value.get('flag')
            type = value.get('type', 'string')
        else:
            flag = value
            type = 'string'

        option = options.get(key)

        if type == 'boolean':
            if option is not None and (option is True or option.lower() in ["true", "yes", "y", "1"]):
                args.append(flag)
        elif type == 'string':
            if option is not None and option != "":
                args.append(flag)
                args.append(option)

    return args


ds_host = os.getenv('DS_HOST', socket.gethostname())
ds_master_host = os.getenv('DS_MASTER_HOST')

setup_metadata = OrderedDict()
setup_metadata['DS_ACCEPT_LICENSE'] = {'flag': '--acceptLicense', 'type': 'boolean', 'default': True}
setup_metadata['DS_ADMIN_PORT'] = {'flag': '--adminConnectorPort', 'default': '4444'}
setup_metadata['DS_CERT_NICKNAME'] = '--certNickname'
setup_metadata['DS_ROOT_USER_DN'] = {'flag': '--rootUserDn', 'default': "cn=Directory Manager"}
setup_metadata['DS_ROOT_USER_PASSWORD_FILE'] = '--rootUserPasswordFile'
setup_metadata['DS_ROOT_USER_PASSWORD'] = '--rootUserPassword'
setup_metadata['DS_DO_NOT_START'] = {'flag': '--doNotStart', 'type': 'boolean', 'default': True}
setup_metadata['DS_INSTANCE_PATH'] = {'flag': '--instancePath', 'default': os.path.join(os.getcwd(), 'opendj')}
setup_metadata['DS_KEY_STORE_PASSWORD'] = '--keyStorePassword'
setup_metadata['DS_KEY_STORE_PASSWORD_FILE'] = '--keyStorePasswordFile'
setup_metadata['DS_QUIET_MODE'] = {'flag': '--quiet', 'type': 'boolean'}
setup_metadata['DS_SKIP_PORT_CHECK'] = {'flag': '--skipPortCheck', 'type': 'boolean'}
setup_metadata['DS_JAVA_KEY_STORE'] = '--useJavaKeyStore'
setup_metadata['DS_JCEKS_KEY_STORE'] = '--useJceks'
setup_metadata['DS_PKCS11_KEY_STORE'] = '--usePkcs11KeyStore'
setup_metadata['DS_PKCS12_KEY_STORE'] = '--usePkcs12KeyStore'
setup_metadata['DS_PRODUCTION_MODE'] = {'flag': '--productionMode', 'type': 'boolean', 'default': True}
setup_metadata['DS_ENABLE_START_TLS'] = {'flag': '--enableStartTls', 'type': 'boolean', 'default': True}
setup_metadata['DS_LDAP_PORT'] = {'flag': '--ldapPort'}
setup_metadata['DS_LDAPS_PORT'] = {'flag': '--ldapsPort'}
setup_metadata['DS_ADD_BASE_ENTRY'] = {'flag': '--addBaseEntry', 'type': 'boolean', 'default': True}
setup_metadata['DS_BACKEND_TYPE'] = {'flag': '--backendType', 'default': 'je-backend'}
setup_metadata['DS_BASE_DN'] = {'flag': '--baseDn', 'default': 'dc=openam,dc=forgerock,dc=org'}
setup_metadata['DS_LDIF_FILE'] = '--ldifFile'
setup_metadata['DS_REJECT_FILE'] = '--rejectFile'
setup_metadata['DS_SAMPLE_DATA'] = '--sampleData'
setup_metadata['DS_SKIP_FILE'] = '--skipFile'
setup_metadata['DS_HOST'] = {'flag': '--hostname', 'default': ds_host}
setup_metadata['DS_HTTP_PORT'] = {'flag': '--httpPort'}
setup_metadata['DS_HTTPS_PORT'] = {'flag': '--httpsPort'}

setup_options = read_options(setup_metadata)

if setup_options['DS_LDAP_PORT'] is None:
    setup_options['DS_LDAP_PORT'] = '1689'
if setup_options['DS_HTTP_PORT'] is None:
    setup_options['DS_HTTP_PORT'] = '8080'

if setup_options['DS_ENABLE_START_TLS'] is True:
    if setup_options['DS_LDAPS_PORT'] is None:
        setup_options['DS_LDAPS_PORT'] = '1636'
    if setup_options['DS_HTTPS_PORT'] is None:
        setup_options['DS_HTTPS_PORT'] = '8443'

setup_args = build_args(setup_options, setup_metadata)

setup_repl_metadata = OrderedDict()
setup_repl_metadata['DS_REPL_BASE_DN'] = {'flag': '--baseDn', 'default': setup_options.get('DS_BASE_DN')}
setup_repl_metadata['DS_REPL_ADMIN_PASSWORD'] = {'flag': '--adminPassword',
                                                 'default': setup_options.get('DS_ROOT_USER_PASSWORD')}
setup_repl_metadata['DS_REPL_ADMIN_PASSWORD_FILE'] = {'flag': '--adminPasswordFile',
                                                      'default': setup_options.get('DS_ROOT_USER_PASSWORD_FILE')}
setup_repl_metadata['DS_REPL_CONNECT_TIMEOUT'] = '--connectTimeout'
setup_repl_metadata['DS_REPL_ADVANCED'] = {'flag': '--advanced', 'type': 'boolean'}
setup_repl_metadata['DS_REPL_ADMIN_UID'] = {'flag': '--adminUid', 'default': 'admin'}
setup_repl_metadata['DS_REPL_SASL_OPTION'] = '--saslOption'
setup_repl_metadata['DS_REPL_TRUST_ALL'] = {'flag': '--trustAll', 'type': 'boolean'}
setup_repl_metadata['DS_REPL_TRUST_STORE_PATH'] = '--trustStorePath'
setup_repl_metadata['DS_REPL_TRUST_STORE_PASSWORD'] = '--trustStorePassword'
setup_repl_metadata['DS_REPL_TRUST_STORE_PASSWORD_FILE'] = '--trustStorePasswordFile'
setup_repl_metadata['DS_REPL_KEY_STORE_PATH'] = '--keyStorePath'
setup_repl_metadata['DS_REPL_KEY_STORE_PASSWORD'] = '--keyStorePassword'
setup_repl_metadata['DS_REPL_KEY_STORE_PASSWORD_FILE'] = '--keyStorePasswordFile'
setup_repl_metadata['DS_REPL_CERT_NICKNAME'] = '--certNickname'
setup_repl_metadata['DS_REPL_QUIET'] = {'flag': '--quiet', 'type': 'boolean'}
setup_repl_metadata['DS_REPL_NO_PROMPT'] = {'flag': '--no-prompt', 'type': 'boolean', 'default': True}
setup_repl_metadata['DS_REPL_PROPERTIES_FILE_PATH'] = '--propertiesFilePath'
setup_repl_metadata['DS_REPL_NO_PROPERTIES_FILE'] = {'flag': '--noPropertiesFile', 'type': 'boolean'}
setup_repl_metadata['DS_REPL_HOST_1'] = {'flag': '--host1', 'default': setup_options.get('DS_HOST')}
setup_repl_metadata['DS_REPL_PORT_1'] = {'flag': '--port1', 'default': setup_options.get('DS_ADMIN_PORT')}
setup_repl_metadata['DS_REPL_BIND_DN_1'] = {'flag': '--bindDn1', 'default': setup_options.get('DS_ROOT_USER_DN')}
setup_repl_metadata['DS_REPL_BIND_PASSWORD_1'] = {'flag': '--bindPassword1',
                                                  'default': setup_options.get('DS_ROOT_USER_PASSWORD')}
setup_repl_metadata['DS_REPL_BIND_PASSWORD_FILE_1'] = {'flag': '--bindPasswordFile1',
                                                       'default': setup_options.get('DS_ROOT_USER_PASSWORD_FILE')}
setup_repl_metadata['DS_REPL_REPLICATION_PORT_1'] = {'flag': '--replicationPort1',
                                                     'default': '58989'}
setup_repl_metadata['DS_REPL_SECURE_REPLICATION_1'] = {'flag': '--secureReplication1', 'type': 'boolean'}
setup_repl_metadata['DS_REPL_NO_REPLICATION_SERVER_1'] = {'flag': '--noReplicationServer1', 'type': 'boolean'}
setup_repl_metadata['DS_REPL_ONLY_REPLICATION_SERVER_1'] = {'flag': '--onlyReplicationServer1', 'type': 'boolean'}
setup_repl_metadata['DS_REPL_HOST_2'] = {'flag': '--host2', 'default': ds_master_host}
setup_repl_metadata['DS_REPL_PORT_2'] = {'flag': '--port2', 'default': '4444'}
setup_repl_metadata['DS_REPL_BIND_DN_2'] = {'flag': '--bindDn2', 'default': setup_options.get('DS_ROOT_USER_DN')}
setup_repl_metadata['DS_REPL_BIND_PASSWORD_2'] = {'flag': '--bindPassword2',
                                                  'default': setup_options.get('DS_ROOT_USER_PASSWORD')}
setup_repl_metadata['DS_REPL_BIND_PASSWORD_FILE_2'] = {'flag': '--bindPasswordFile2',
                                                       'default': setup_options.get('DS_ROOT_USER_PASSWORD_FILE')}
setup_repl_metadata['DS_REPL_REPLICATION_PORT_2'] = {'flag': '--replicationPort2', 'default': '50889'}
setup_repl_metadata['DS_REPL_SECURE_REPLICATION_2'] = {'flag': '--secureReplication2', 'type': 'boolean'}
setup_repl_metadata['DS_REPL_NO_REPLICATION_SERVER_2'] = {'flag': '--noReplicationServer2', 'type': 'boolean'}
setup_repl_metadata['DS_REPL_ONLY_REPLICATION_SERVER_2'] = {'flag': '--onlyReplicationServer2', 'type': 'boolean'}
setup_repl_metadata['DS_REPL_SKIP_PORT_CHECK'] = {'flag': '--skipPortCheck', 'type': 'boolean'}
setup_repl_metadata['DS_REPL_NO_SCHEMA_REPLICATION'] = {'flag': '--noSchemaReplication', 'type': 'boolean'}
setup_repl_metadata['DS_REPL_USE_SECOND_SERVER_AS_SCHEMA_SOURCE'] = {'flag': '--useSecondServerAsSchemaSource',
                                                                     'type': 'boolean'}

initialize_repl_metadata = OrderedDict()
initialize_repl_metadata['DS_REPL_BASE_DN'] = {'flag': '--baseDn', 'default': setup_options.get('DS_BASE_DN')}
initialize_repl_metadata['DS_REPL_ADMIN_PASSWORD'] = {'flag': '--adminPassword',
                                                      'default': setup_options.get('DS_ROOT_USER_PASSWORD')}
initialize_repl_metadata['DS_REPL_ADMIN_PASSWORD_FILE'] = {'flag': '--adminPasswordFile',
                                                           'default': setup_options.get('DS_ROOT_USER_PASSWORD_FILE')}
initialize_repl_metadata['DS_REPL_CONNECT_TIMEOUT'] = '--connectTimeout'
initialize_repl_metadata['DS_REPL_ADVANCED'] = {'flag': '--advanced', 'type': 'boolean'}
initialize_repl_metadata['DS_REPL_ADMIN_UID'] = {'flag': '--adminUid', 'default': 'admin'}
initialize_repl_metadata['DS_REPL_SASL_OPTION'] = '--saslOption'
initialize_repl_metadata['DS_REPL_TRUST_ALL'] = {'flag': '--trustAll', 'type': 'boolean'}
initialize_repl_metadata['DS_REPL_TRUST_STORE_PATH'] = '--trustStorePath'
initialize_repl_metadata['DS_REPL_TRUST_STORE_PASSWORD'] = '--trustStorePassword'
initialize_repl_metadata['DS_REPL_TRUST_STORE_PASSWORD_FILE'] = '--trustStorePasswordFile'
initialize_repl_metadata['DS_REPL_KEY_STORE_PATH'] = '--keyStorePath'
initialize_repl_metadata['DS_REPL_KEY_STORE_PASSWORD'] = '--keyStorePassword'
initialize_repl_metadata['DS_REPL_KEY_STORE_PASSWORD_FILE'] = '--keyStorePasswordFile'
initialize_repl_metadata['DS_REPL_CERT_NICKNAME'] = '--certNickname'
initialize_repl_metadata['DS_REPL_QUIET'] = {'flag': '--quiet', 'type': 'boolean'}
initialize_repl_metadata['DS_REPL_NO_PROMPT'] = {'flag': '--no-prompt', 'type': 'boolean', 'default': True}
initialize_repl_metadata['DS_REPL_PROPERTIES_FILE_PATH'] = '--propertiesFilePath'
initialize_repl_metadata['DS_REPL_NO_PROPERTIES_FILE'] = {'flag': '--noPropertiesFile', 'type': 'boolean'}
initialize_repl_metadata['DS_REPL_HOST_1'] = {'flag': '--hostDestination', 'default': setup_options.get('DS_HOST')}
initialize_repl_metadata['DS_REPL_PORT_1'] = {'flag': '--portDestination',
                                              'default': setup_options.get('DS_ADMIN_PORT')}
initialize_repl_metadata['DS_REPL_HOST_2'] = {'flag': '--hostSource', 'default': ds_master_host}
initialize_repl_metadata['DS_REPL_PORT_2'] = {'flag': '--portSource', 'default': '4444'}

setup_repl_options = read_options(setup_repl_metadata)
initialize_repl_options = read_options(initialize_repl_metadata)

if setup_repl_options.get('DS_REPL_ADMIN_PASSWORD') is None and setup_repl_options.get(
        'DS_REPL_ADMIN_PASSWORD_FILE') is None:
    setup_repl_options['DS_REPL_ADMIN_PASSWORD'] = 'xxxxxxxx'

if len(sys.argv) == 1 or 'setup' in sys.argv:
    setup_command = [os.path.join(os.getcwd(), 'opendj', 'setup'), 'directory-server'] + setup_args
    print ' '.join(setup_command)
    subprocess.check_call(setup_command, cwd=os.path.join(os.getcwd(), 'opendj'))

if 'dsreplication' in sys.argv:
    if len(sys.argv) == 2 or 'enable' in sys.argv:
        setup_repl_args = build_args(setup_repl_options, setup_repl_metadata)
        setup_repl_command = [os.path.join(os.getcwd(), 'opendj', 'bin', 'dsreplication'),
                              'configure'] + setup_repl_args
        print ' '.join(setup_repl_command)
        subprocess.check_call(setup_repl_command, cwd=os.path.join(os.getcwd(), 'opendj', 'bin'))
    elif 'initialize' in sys.argv:
        initialize_repl_args = build_args(initialize_repl_options, initialize_repl_metadata)
        initialize_repl_command = [os.path.join(os.getcwd(), 'opendj', 'bin', 'dsreplication'),
                                   'initialize'] + initialize_repl_args
        print ' '.join(initialize_repl_command)
        subprocess.check_call(initialize_repl_command, cwd=os.path.join(os.getcwd(), 'opendj', 'bin'))

