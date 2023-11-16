# ------------------------------------------------------------------------------
# Prod build:  docker build -t libcal-bookings .
# Prod run:    docker run --rm -it --name libcal-bookings --network=docker-environment_default -p 8080:8080 libcal-bookings
# ------------------------------------------------------------------------------

FROM registry.gitlab.com/byuhbll/apps/images/django:3.2-python3.8

# create app user and group
RUN set -ex \
    && addgroup --gid 2000 appgroup \
    && adduser --system \
      --disabled-password \
      --no-create-home \
      --ingroup appgroup \
      --uid 1000 appuser

# Get app requirements
COPY requirements /requirements

RUN set -ex \
    && apt-get update && apt-get install -y procps --no-install-recommends \
    # pip
    && pip install --no-cache-dir -U pip \
    && pip install --no-cache-dir -r /requirements/prod.txt \
    # Cleanup
    && rm -rf /var/lib/apt/lists/* \
    && rm -rf /requirements

# ------------------------------------------------------------------------------

WORKDIR /code
COPY . /code

RUN set -ex \
    && rm -rf /code/node_modules \
    && chown -R appuser:appgroup /code

USER appuser
EXPOSE 8080

ENTRYPOINT ["bash", "/code/project/entrypoint.prod.sh"]
CMD ["uwsgi", "--ini", "/code/project/uwsgi.ini"]
