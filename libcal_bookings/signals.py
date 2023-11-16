"""Signals"""
import logging

from django.db.models.signals import (  # noqa: F401 imported but never used
    pre_delete,
)
from django.dispatch import receiver  # noqa: F401 imported but never used

# from .models import ExampleModel

logger = logging.getLogger(__name__)


# Define signal receivers here. An example receiver is shown below.
# See https://docs.djangoproject.com/en/3.2/topics/signals/ for more
# information on signals.

# @receiver(pre_delete, sender=ExampleModel)
# def on_delete_do_something(sender, instance, using, **kwargs):
#     instance.do_something()
