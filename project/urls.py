from django.urls import include, path
from dry.urls import urlpatterns as dry_urlpatterns

from libcal_bookings import urls as libcal_bookings_urls

urlpatterns = []

project_urlpatterns = [
    # libcal_bookings app urls
    path('', include((libcal_bookings_urls, 'libcal_bookings')))
]

urlpatterns = project_urlpatterns + dry_urlpatterns
