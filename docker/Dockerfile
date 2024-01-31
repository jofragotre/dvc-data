FROM python:3.10-slim

ARG USER_ID
ARG USER_NAME
ENV HOME=/home/${USER_NAME} \
    VIRTUAL_ENV=/home/${USER_NAME}/venv
ENV \
  PYTHONUNBUFFERED=1 \
  DEBIAN_FRONTEND=noninteractive \
  TZ=Europe/Warsaw \
  PATH="/usr/local/gcloud/google-cloud-sdk/bin:${HOME}/.local/bin:${VIRTUAL_ENV}/bin:${PATH}" \
  PYTHONPATH="/app:${PYTHONPATH}" \
  BUILD_POETRY_LOCK="${HOME}/poetry.lock.build"

RUN apt-get -qq update \
    && apt-get -qq -y install vim gcc curl git build-essential libb64-dev software-properties-common \
    && rm -rf /var/lib/apt/lists/* \
    && apt-get -qq -y clean

RUN curl https://dl.google.com/dl/cloudsdk/channels/rapid/downloads/google-cloud-sdk-426.0.0-linux-x86_64.tar.gz > /tmp/google-cloud-sdk.tar.gz
RUN mkdir -p /usr/local/gcloud \
    && tar -C /usr/local/gcloud -xf /tmp/google-cloud-sdk.tar.gz \
    && /usr/local/gcloud/google-cloud-sdk/install.sh --usage-reporting false --command-completion true --bash-completion true --path-update true --quiet

RUN addgroup --system --gid ${USER_ID} ${USER_NAME} \
    && useradd --system -m --no-log-init --home-dir ${HOME} --uid ${USER_ID} --gid ${USER_NAME} --groups ${USER_NAME} ${USER_NAME}

RUN chown -R ${USER_NAME}:${USER_NAME} ${HOME}
RUN mkdir -p /app && chown -R ${USER_NAME}:${USER_NAME} /app /tmp

RUN curl -sSL https://install.python-poetry.org | python3 - --version 1.7.1

USER ${USER_NAME}

COPY pyproject.toml *.lock /app/
WORKDIR /app

RUN poetry config virtualenvs.create false \
    && python3.10 -m venv ${VIRTUAL_ENV} \
    && pip install --upgrade pip setuptools \
    && poetry install && cp poetry.lock ${BUILD_POETRY_LOCK} \
    && rm -rf ${HOME}/.cache/*

USER root
COPY ./docker/scripts/* /
RUN chown -R ${USER_NAME} /*.sh && chmod +x /*.sh
USER ${USER_NAME}

RUN git config --global user.email "jofragotre@gmail.com" \
    && git config --global user.name "jofragotre"

ENV GDRIVE_CREDENTIALS_DATA='{"access_token": "ya29.a0AfB_byAA8WQ4WBkvXp_L_ceEbR0N-AXUwVOutzXKvzulqfacIgid0lOtfr6JgVNIyVZ93GNqdG3fBdwIuG0bnWUA_W5nXtIKl-kJAn277ZTptmJqhMF-mbNGPjczt_-jg8cLp2-t332i-tzbX51E1jNqCyQfxymzAoD7-AaCgYKAfgSARMSFQHGX2MiNxbqWYoJjjCEGmtDbedaqg0173", "client_id": "710796635688-iivsgbgsb6uv1fap6635dhvuei09o66c.apps.googleusercontent.com", "client_secret": "a1Fz59uTpVNeG_VGuSKDLJXv", "refresh_token": "1//036BFqxnX4pbrCgYIARAAGAMSNwF-L9Irl4u_WyHQlSCxj7cmxynh41aEu-5ucbcKMVeu6fyA38hJMNuSp03wytM9J84cCA8St6Y", "token_expiry": "2024-01-31T17:36:08Z", "token_uri": "https://oauth2.googleapis.com/token", "user_agent": null, "revoke_uri": "https://oauth2.googleapis.com/revoke", "id_token": null, "id_token_jwt": null, "token_response": {"access_token": "ya29.a0AfB_byAA8WQ4WBkvXp_L_ceEbR0N-AXUwVOutzXKvzulqfacIgid0lOtfr6JgVNIyVZ93GNqdG3fBdwIuG0bnWUA_W5nXtIKl-kJAn277ZTptmJqhMF-mbNGPjczt_-jg8cLp2-t332i-tzbX51E1jNqCyQfxymzAoD7-AaCgYKAfgSARMSFQHGX2MiNxbqWYoJjjCEGmtDbedaqg0173", "expires_in": 3599, "scope": "https://www.googleapis.com/auth/drive.appdata https://www.googleapis.com/auth/drive", "token_type": "Bearer"}, "scopes": ["https://www.googleapis.com/auth/drive", "https://www.googleapis.com/auth/drive.appdata"], "token_info_uri": "https://oauth2.googleapis.com/tokeninfo", "invalid": false, "_class": "OAuth2Credentials", "_module": "oauth2client.client"}'

COPY . /app/
CMD ["/startup-script.sh"]
