#-*- coding: utf-8 -*-

from __future__ import unicode_literals
import json

from django.http import Http404, HttpResponse

from infinite_scroll_pagination import paginator
from infinite_scroll_pagination import serializers

from .models import Article


def pagination_ajax(request):
    if not request.is_ajax():
        return Http404()

    try:
        value, pk = serializers.page_key(request.GET.get('p', ''))
    except serializers.InvalidPage:
        return Http404()

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
            'next_page': serializers.to_page_key(**page.next_page()),
            'prev_page': serializers.to_page_key(**page.prev_page())}

    return HttpResponse(json.dumps(data), content_type="application/json")
