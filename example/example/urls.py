from django.conf.urls import patterns, include, url

import light.urls

urlpatterns = patterns('',
    url(r'^$', include(light.urls)),
)
