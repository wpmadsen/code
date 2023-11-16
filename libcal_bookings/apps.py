"""
Boilerplate.
"""
import logging

from django.apps import AppConfig

logger = logging.getLogger(__name__)


class LibcalBookingsConfig(AppConfig):
    name = 'libcal_bookings'
    verbose_name = 'Libcal Bookings'

    def ready(self):
        from . import signals  # noqa: F401
