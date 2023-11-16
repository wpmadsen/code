# -----------------------------------------------------------------------------
# Development entrypoint
# This is run whenever the development Docker container is started.
# -----------------------------------------------------------------------------

# Create initial application.yml file if it doesn't exist
if [ ! -f /code/application.yml ]; then
    echo "extends: \"project/application-base.yml\"" > /code/application.yml
fi

# Install the pre-commit hooks
pre-commit install

# Run migrations
export DJANGO_CONFIG=application.yml
create-pg-db
python manage.py migrate --noinput
python manage.py createsuperuser \
    --no-color \
    -v0 \
    --noinput \
    --username="$SUPERUSER" \
    --email="$SUPERUSER@byu.edu" \
|| true

# Install Node modules if they aren't already there
if [ ! -d /code/node_modules/ ]; then
    npm install
fi

# Executes whatever command is passed in.
# If you want to have it just wait you could pass in `tail /dev/null`
$@
