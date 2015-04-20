import os

from django.conf import settings
from django.core.exceptions import ImproperlyConfigured

# this deliberately HAS a slash at the end to make sure it joins
# correctly with the parsed urls
OFFLINECDN_STATIC_URL = getattr(settings, 'OFFLINECDN_STATIC_URL',
                                settings.STATIC_URL)

# OFFLINECDN_STATIC_ROOT must be specified in the configuration and added to
# STATICFILES_DIRS
OFFLINECDN_STATIC_ROOT = getattr(settings, 'OFFLINECDN_STATIC_ROOT', None)
if OFFLINECDN_STATIC_ROOT is None:
    raise ImproperlyConfigured("OFFLINECDN_STATIC_ROOT is not specified")

# this controls whether or not we're in offline mode. defaults to DEBUG
OFFLINECDN_MODE = getattr(settings, 'OFFLINECDN_MODE', settings.DEBUG)
