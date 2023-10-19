# See here for image contents: https://github.com/microsoft/vscode-dev-containers/tree/v0.209.6/containers/java-8/.devcontainer/base.Dockerfile

# [Choice] Debian OS version (use bullseye on local arm64/Apple Silicon): buster, bullseye
ARG VARIANT="bullseye"
FROM mcr.microsoft.com/vscode/devcontainers/java:0-8-${VARIANT}

# [Option] Install Maven
ARG INSTALL_MAVEN="true"
ARG MAVEN_VERSION="3.8.5"
# [Option] Install Gradle
ARG INSTALL_GRADLE="false"
ARG GRADLE_VERSION=""

ARG PYTHON_VERSION="3.10"
ARG PYTHON_PATH=/usr/local/python
ENV PIPX_HOME=/usr/local/py-utils \
    PIPX_BIN_DIR=/usr/local/py-utils/bin
ENV PATH=${PYTHON_PATH}/bin:${PATH}:${PIPX_BIN_DIR}

RUN if [ "${INSTALL_MAVEN}" = "true" ]; then su vscode -c "umask 0002 && . /usr/local/sdkman/bin/sdkman-init.sh && sdk install maven \"${MAVEN_VERSION}\""; fi \
    && if [ "${INSTALL_GRADLE}" = "true" ]; then su vscode -c "umask 0002 && . /usr/local/sdkman/bin/sdkman-init.sh && sdk install gradle \"${GRADLE_VERSION}\""; fi

# [Choice] Node.js version: none, lts/*, 16, 14, 12, 10
ARG NODE_VERSION="lts/*"
RUN if [ "${NODE_VERSION}" != "none" ]; then su vscode -c "umask 0002 && . /usr/local/share/nvm/nvm.sh && nvm install ${NODE_VERSION} 2>&1"; fi

# [Optional] Uncomment this section to install additional OS packages.
RUN apt-get update && export DEBIAN_FRONTEND=noninteractive \
    && apt-get -y install --no-install-recommends librdkafka-dev

# [Optional] Uncomment this line to install global node packages.
# RUN su vscode -c "source /usr/local/share/nvm/nvm.sh && npm install -g <your-package-here>" 2>&1

RUN apt-get update && export DEBIAN_FRONTEND=noninteractive  \
    && apt-get -y install --no-install-recommends curl ca-certificates \
    && bash -c "$(curl -fsSL "https://raw.githubusercontent.com/microsoft/vscode-dev-containers/main/script-library/python-debian.sh")" -- "${PYTHON_VERSION}" "${PYTHON_PATH}" "${PIPX_HOME}" \
    && apt-get clean -y && rm -rf /var/lib/apt/lists/*

# # Install Cue-lang
# RUN wget https://github.com/cue-lang/cue/releases/download/v0.4.2/cue_v0.4.2_linux_amd64.tar.gz -C /tmp
# RUN cp /tmp/cue /bin/cue

USER vscode

# Install Poetry
RUN curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python -
ENV PATH "$PATH:/home/vscode/.poetry/bin"

# We don't need virtualenvs in a DevEnvironment
RUN poetry config virtualenvs.create false

RUN mkdir -p ~/deps

RUN wget --content-disposition https://github.com/siddhi-io/siddhi-sdk/releases/download/v5.1.2/siddhi-sdk-5.1.2.zip -O ~/deps/siddhi-sdk.zip
RUN unzip ~/deps/siddhi-sdk.zip -d ~/deps
RUN rm ~/deps/*.zip
RUN mv ~/deps/siddhi-sdk-* ~/deps/siddhi-sdk

# RUN wget --content-disposition https://github.com/siddhi-io/PySiddhi/releases/download/v5.1.0/siddhi-python-api-proxy-5.1.0.jar -P ~/deps/siddhi-sdk/lib/

ENV SIDDHISDK_HOME "/home/vscode/deps/siddhi-sdk"