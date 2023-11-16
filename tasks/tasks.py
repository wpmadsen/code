#!/usr/bin/env python
"""
Invoke task list for the build process.
"""
import threading
from pathlib import Path

from invoke import Collection, task

PORT = 8080

# ----------------------------------------------------------------------------
# Gulp helper

GULPFILEPATH = 'tasks/gulpfile.js'


def _gulp(c, command):
    c.run(f'gulp -f {GULPFILEPATH} {command}', pty=True, in_stream=False)


# ----------------------------------------------------------------------------
# Server tasks (run, uwsgi)


@task
def server_run(c, host='0.0.0.0', port=PORT):
    """
    Runs the Django dev server.
    """
    c.run(f'python manage.py runserver_plus {host}:{port}', pty=True)


@task
def server_livereload(c, files=None, options=''):
    """
    Runs the Django livereload server. If you're going to run this manually,
    do it in another console.
    """
    files = files if files else 'config.yml project/*.yml **/*.html **/*.py'
    c.run(
        f'python manage.py livereload {files} {options}',
        pty=True,
        in_stream=False,
    )


@task
def server_uwsgi(c, path='.configs/uwsgi.ini'):
    """
    Runs the app via a uwsgi server. Expects to find the uwsgi.ini file in
    the .configs/ directory.
    """
    c.run(f'uwsgi {path}', pty=True)


# ----------------------------------------------------------------------------
# Static tasks (watch, build, clean)


@task
def static_watch(c):
    """
    Uses Gulp to build the frontend static content and put it in
    libcal_bookings/static, and to keep watching the assets/
    directories for changes. Cleans the static files out first (via Gulp).
    """
    _gulp(c, 'watch')


@task
def static_build(c):
    """
    Uses Gulp to build the frontend static content and put it in
    libcal_bookings/static. Cleans the static files out first
    (via Gulp).
    """
    _gulp(c, 'build')


@task
def static_css(c):
    """
    Uses Gulp to build the CSS.
    """
    _gulp(c, 'css')


@task
def static_css_watch(c):
    """
    Uses Gulp to watch CSS assets and build CSS when anything changes.
    """
    _gulp(c, 'cssWatch')


@task
def static_js(c):
    """
    Uses Gulp to build the JS.
    """
    _gulp(c, 'js')


@task
def static_js_watch(c):
    """
    Uses Gulp to watch JS assets and build JS when anything changes.
    """
    _gulp(c, 'jsWatch')


@task
def static_copy(c):
    """
    Uses Gulp to copy the static files.
    """
    _gulp(c, 'copy')


@task
def static_copy_watch(c):
    """
    Uses Gulp to watch static paths and copy files when anything changes.
    """
    _gulp(c, 'copyWatch')


@task
def static_clean(c):
    """
    Uses Gulp to delete everything in libcal_bookings/static.
    """
    _gulp(c, 'clean')


# ----------------------------------------------------------------------------
# Top-level tasks


@task
def run(
    c,
    host='0.0.0.0',
    port=PORT,
    nostatic=False,
    nolivereload=False,
    livereload_files=None,
    livereload_options='',
):
    """
    Runs the Django dev server, the Django livereload server, and (if present)
    the Gulp static watchers.

    To run just the dev server: inv run --nostatic --nolivereload
    (This is the same as inv server.run)
    """
    if not nostatic and Path(GULPFILEPATH).exists():
        # Run the static file watcher in a separate thread so we can have
        # it run in parallel with the Django dev server
        t = threading.Thread(target=lambda: static_watch(c), daemon=True)
        t.start()

    if not nolivereload:
        # Run the Django livereload server in a separate thread
        # If you don't want this, pass in --livereload false
        t = threading.Thread(
            target=lambda: server_livereload(
                c, livereload_files, livereload_options
            ),
            daemon=True,
        )
        t.start()

    # Start the Django dev server
    server_run(c, host=host, port=port)


@task
def manage(c, command, options=''):
    """
    Runs ./manage.py with a command.
    """
    c.run(f'python manage.py {command} {options}', pty=True)


@task
def refreshdb(c):
    """
    Runs ./manage.py reset_db --noinput && ./manage.py migrate &&
    ./manage.py createsuperuser
    """
    manage(c, 'reset_db', '--noinput')
    manage(c, 'migrate')
    manage(c, 'createsuperuser')


@task
def makemigrations(c, options=''):
    """
    Runs ./manage.py makemigrations with an optional "options" parameter.
    """
    manage(c, 'makemigrations', options)


@task
def migrate(c, options=''):
    """
    Runs ./manage.py migrate.
    """
    manage(c, 'migrate', options)


@task
def shell(c):
    """
    Runs ./manage.py shell_plus.
    """
    manage(c, 'shell_plus')


# ----------------------------------------------------------------------------

ns = Collection()

ns.add_task(run)
ns.add_task(manage)
ns.add_task(refreshdb)
ns.add_task(makemigrations)
ns.add_task(migrate)
ns.add_task(shell)


static = Collection('static')
static.add_task(static_build, 'build')
static.add_task(static_watch, 'watch')
static.add_task(static_clean, 'clean')
static.add_task(static_css, 'css')
static.add_task(static_css_watch, 'css:watch')
static.add_task(static_js, 'js')
static.add_task(static_js_watch, 'js:watch')
static.add_task(static_copy, 'copy')
static.add_task(static_copy_watch, 'copy:watch')
ns.add_collection(static)


server = Collection('server')
server.add_task(server_run, 'run')
server.add_task(server_livereload, 'livereload')
server.add_task(server_uwsgi, 'uwsgi')
ns.add_collection(server)


# App-specific tasks below

# @task
# def custom_task(c, parameter=param):
#     c.run('something', pty=True)

# ----------------------------------------------------------------------------

# (ns is from dry.tasks)
# ns.add_task(custom_task)
