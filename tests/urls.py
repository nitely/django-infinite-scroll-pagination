#-*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.conf.urls import include, url

import tests.views


urlpatterns = [
    url(r'^page/$', tests.views.pagination_ajax, name='pagination-ajax'),
    url(r'^page/(?P<pk>\d+)/$', tests.views.pagination_ajax, name='pagination-ajax'),
]
