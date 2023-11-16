"""
Signals.
"""
import logging

from django.conf import settings
from django.contrib.auth.signals import user_logged_in
from dry.signals import update_user_info  # noqa: F401 imported but not used

from .models import User

logger = logging.getLogger(__name__)


def update_user_info_signal(sender, request, user, **kwargs):
    """
    Function used as a Django signal receiver, called when a user logs into
    the site successfully.

    If dry.user_info_signal setting is enabled, this will:
        - Make the first user a superuser (and staff)
        - Update users information from the university system (uses bayou,
        so credentials must be present in config)
    """
    if settings.DRY['USER_INFO_SIGNAL']:
        if user.pk == 1:
            user.is_superuser = True
            user.is_staff = True
            user.save()

        update_user_info(user)


# Hook up the signal
user_logged_in.connect(update_user_info_signal, sender=User)
