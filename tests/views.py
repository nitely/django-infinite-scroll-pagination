#-*- coding: utf-8 -*-

from __future__ import unicode_literals
import json
import re
import time
from datetime import datetime

from django.http import Http404, HttpResponse

from infinite_scroll_pagination import paginator

from .models import Article

PAGE_RE = re.compile(r'^(?P<value>[0-9]+\.[0-9]+)-(?P<pk>[0-9]+)$')


# XXX move to lib
def page_key(raw_page):
    if not raw_page:
        return None, None
    m = re.match(PAGE_RE, raw_page)
    if m is None:
        raise Http404()
    try:
        timestamp = datetime.fromtimestamp(float(m.group('value')))
    except (OverflowError, ValueError):
        raise Http404()
    return timestamp, m.group('pk')


def to_page_key(value=None, pk=None):
    if value is None:
        return ''
    try:
        timestamp = value.timestamp()
    except AttributeError:
        timestamp = time.mktime(value.timetuple())
    return '{}-{}'.format(timestamp, pk)


def pagination_ajax(request):
    if not request.is_ajax():
        return Http404()

    value, pk = page_key(request.GET.get('p', ''))

    try:
        page = paginator.paginate(
            query_set=Article.objects.all(),
            lookup_field='-date',
            value=value,
            pk=pk,
            per_page=20,
            move_to=paginator.NEXT_PAGE)
    except paginator.EmptyPage:
        data = {'error': "this page is empty"}
    else:
        data = {
            'articles': [{'title': article.title} for article in page],
            'has_next': page.has_next(),
            'has_prev': page.has_previous(),
            'next_objects_left': page.next_objects_left(limit=100),
            'prev_objects_left': page.prev_objects_left(limit=100),
            'next_pages_left': page.next_pages_left(limit=100),
            'prev_pages_left': page.prev_pages_left(limit=100),
            'next_page': to_page_key(**page.next_page()),
            'prev_page': to_page_key(**page.prev_page())}

    return HttpResponse(json.dumps(data), content_type="application/json")
