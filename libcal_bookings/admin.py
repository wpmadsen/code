import logging

from django.contrib import admin

logger = logging.getLogger(__name__)

admin.site.site_header = 'LibCal Bookings'
admin.site.site_title = admin.site.site_header
