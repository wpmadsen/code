#!/usr/bin/env python
from os import environ

# Don't import if we're running tests
if not environ.get('RUNNING_TESTS', False):
    from .tasks import (  # noqa F401
        makemigrations,
        manage,
        migrate,
        refreshdb,
        run,
        server_livereload,
        server_run,
        server_uwsgi,
        shell,
        static_build,
        static_clean,
        static_copy,
        static_copy_watch,
        static_css,
        static_css_watch,
        static_js,
        static_js_watch,
        static_watch,
    )
