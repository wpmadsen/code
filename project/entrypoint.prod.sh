# Production entrypoint
# This is run whenever the Docker container is started.
# -----------------------------------------------------------------------------

set -e

mkdir -p /tmp/data

# Create the database if DJANGO_CREATEDB is set to 'on'
if [ "x$DJANGO_CREATEDB" = 'xon' ]; then
    create-pg-db
fi

# Run collectstatic if DJANGO_COLLECTSTATIC is set to 'on'
if [ "x$DJANGO_COLLECTSTATIC" = 'xon' ]; then
    python manage.py collectstatic --noinput
fi

# Run migrations if DJANGO_MIGRATE is set to 'on'
if [ "x$DJANGO_MIGRATE" = 'xon' ]; then
    python manage.py migrate --noinput
fi

#######################################################################
# If you need to set up Kafka topics or Solr collections, do that here.
#######################################################################


#######################################################################
# Execute whatever commands were passed in
#######################################################################
$@
