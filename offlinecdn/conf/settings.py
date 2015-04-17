import os

from django.conf import settings

OFFLINE_STATIC_URL = getattr(settings, 'OFFLINE_STATIC_URL', 
                             settings.STATIC_URL + '/offlinecdn')

OFFLINE_STATIC_ROOT = getattr(settings, 'OFFLINE_STATIC_ROOT', 
                              os.path.join(settings.STATIC_ROOT, 'offlinecdn', ''))
