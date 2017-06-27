FROM samloh84/apache-tomcat:8.5.15

ARG VENDOR=forgerock
ARG PRODUCT=ds
ARG PRODUCT_VERSION=5.0.0
ARG TEMP_DIR_ROOT=/tmp/${VENDOR}-${PRODUCT}
ARG TEMP_DIR=${TEMP_DIR_ROOT}/${PRODUCT_VERSION}
ARG INSTALL_DIR_ROOT=/opt/${VENDOR}-${PRODUCT}
ARG INSTALL_DIR=${INSTALL_DIR_ROOT}/${PRODUCT_VERSION}

ARG DS_INSTALL_ZIP=DS-${PRODUCT_VERSION}.zip

COPY ${DS_INSTALL_ZIP} entrypoint.sh setup.py ${TEMP_DIR}/

USER ${ROOT_UID}

RUN \

yum-install which zip unzip && \

mkdir -p ${INSTALL_DIR} && \
pushd ${TEMP_DIR} && \
unzip -qq ${DS_INSTALL_ZIP} -d ${TEMP_DIR} && \

# Move scripts to DS directory
mv ${TEMP_DIR}/entrypoint.sh ${INSTALL_DIR}/entrypoint.sh && \
mv ${TEMP_DIR}/setup.py ${INSTALL_DIR}/setup.py && \
chmod +x ${INSTALL_DIR}/entrypoint.sh && \
chmod +x ${INSTALL_DIR}/setup.py && \

fix-ownership ${INSTALL_DIR} && \
fix-permissions ${INSTALL_DIR} && \
rm -rf ${TEMP_DIR_ROOT} && \
popd

ENV OPENDJ_HOME ${INSTALL_DIR}
ENV PATH ${PATH}:${OPENDJ_HOME}/bin

# HTTP
EXPOSE 8080
# HTTPS
EXPOSE 8443
# REPLICATION PORT 1
EXPOSE 50389
# ADMIN PORT
EXPOSE 4444
# LDAPS PORT
EXPOSE 1636
# LDAP PORT
EXPOSE 1689
# REPLICATION PORT 2
EXPOSE 58989

USER ${APP_UID}

WORKDIR ${OPENDJ_HOME}
CMD ./entrypoint.sh
