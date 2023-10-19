# use siddhi-runner-base
FROM siddhiio/siddhi-runner-base-ubuntu:latest

ARG HOST_BUNDLES_DIR=./siddhi/bundles
ARG HOST_JARS_DIR=./siddhi/jars
ARG JARS=${RUNTIME_SERVER_HOME}/jars
ARG BUNDLES=${RUNTIME_SERVER_HOME}/bundles

# copy bundles & jars to the siddhi-runner distribution
COPY --chown=siddhi_user:siddhi_io ${HOST_BUNDLES_DIR}/ ${BUNDLES}
COPY --chown=siddhi_user:siddhi_io ${HOST_JARS_DIR}/ ${JARS}

# expose ports
EXPOSE 9090 9443 9712 9612 7711 7611 7070 7443

RUN bash ${RUNTIME_SERVER_HOME}/bin/install-jars.sh

STOPSIGNAL SIGINT

ENTRYPOINT ["/home/siddhi_user/siddhi-runner/bin/runner.sh",  "--"]