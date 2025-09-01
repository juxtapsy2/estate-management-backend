FROM docker.io/python:3.12.2-slim-bookworm as python

# Stage 1: Build dependency wheels
FROM python AS python-build-stage

ARG BUILD_ENVIRONMENT=local

RUN apt-get update && apt-get install --no-install-recommends -y \
    build-essential \
    libpq-dev \
 && rm -rf /var/lib/apt/lists/*

WORKDIR /usr/src/app

COPY ./requirements .

RUN pip wheel --wheel-dir /usr/src/app/wheels \
    -r ${BUILD_ENVIRONMENT}.txt

# Stage 2: Python run stage.
FROM python AS python-run-stage 

ARG APP_HOME=/app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV BUILD_ENV ${BUILD_ENVIRONMENT}

WORKDIR ${APP_HOME}

RUN apt-get update && apt-get install --no-install-recommends -y \
    sudo git bash-completion nano ssh \
 && rm -rf /var/lib/apt/lists/*

RUN addgroup --system django && \
    adduser --system --ingroup django django && \
    mkdir -p ${APP_HOME}/staticfiles && \
    chown django:django ${APP_HOME}/staticfiles && \
    chmod 775 ${APP_HOME}/staticfiles
    
RUN apt-get update && apt-get install --no-install-recommends -y \
    libpq-dev \
    gettext \
 && apt-get purge -y --auto-remove -o APT::AutoRemove::RecommendsImportant=false \
 && rm -rf /var/lib/apt/lists/*

COPY --from=python-build-stage /usr/src/app/wheels /wheels

RUN pip install --no-cache-dir --no-index --find-links=/wheels /wheels/* \
    && rm -rf /wheels/

COPY --chown=django:django ./docker/local/django/entrypoint.sh /entrypoint
RUN sed -i 's/\r$//g' /entrypoint && chmod +x /entrypoint

# Start app
COPY --chown=django:django ./docker/local/django/start.sh /start
RUN sed -i 's/\r$//g' /start && chmod +x /start

# Start celery's belongings
COPY --chown=django:django ./docker/local/django/celery/worker/start.sh /start-celeryworker
RUN sed -i 's/\r$//g' /start-celeryworker && chmod +x /start-celeryworker

COPY --chown=django:django ./docker/local/django/celery/beat/start.sh /start-celerybeat
RUN sed -i 's/\r$//g' /start-celerybeat && chmod +x /start-celerybeat

COPY --chown=django:django ./docker/local/django/celery/flower/start.sh /start-flower
RUN sed -i 's/\r$//g' /start-flower && chmod +x /start-flower

COPY --chown=django:django . ${APP_HOME}
RUN chown django:django ${APP_HOME}

USER django

ENTRYPOINT ["/entrypoint"]