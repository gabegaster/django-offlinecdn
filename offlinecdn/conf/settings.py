import os

from django.conf import settings

# this deliberately HAS a slash at the end to make sure it joins
# correctly with the parsed urls
OFFLINE_STATIC_URL = getattr(settings, 'OFFLINE_STATIC_URL', 
                             settings.STATIC_URL + 'offlinecdn/')


OFFLINE_STATIC_ROOT = getattr(settings, 'OFFLINE_STATIC_ROOT', 
                              os.path.join(settings.STATIC_ROOT, 'offlinecdn'))
    

# this controls whether or not we're in offline mode. defaults to DEBUG
OFFLINECDN_MODE = getattr(settings, 'OFFLINECDN_MODE', settings.DEBUG)
