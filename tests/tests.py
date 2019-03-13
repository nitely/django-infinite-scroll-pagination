#-*- coding: utf-8 -*-

from __future__ import unicode_literals
import datetime
import json

from django.test import TestCase
from django.urls import reverse

from django.utils import timezone

from .models import Article
from infinite_scroll_pagination.paginator import SeekPaginator
from infinite_scroll_pagination import paginator as inf_paginator
from infinite_scroll_pagination import serializers


class PaginatorTest(TestCase):

    def setUp(self):
        date = timezone.now()

        for i in range(25):
            seconds = datetime.timedelta(seconds=i)
            Article.objects.create(title="%s" % i, date=date, date_unique=date + seconds)

    def test_paginator_prev_desc(self):
        articles = Article.objects.all().order_by("-date_unique")
        paginator = SeekPaginator(
            Article.objects.all(), per_page=10, lookup_field="-date_unique")
        page_2 = paginator.page(
            value=list(articles)[20].date_unique,
            move_to=inf_paginator.PREV_PAGE)
        self.assertListEqual(list(page_2), list(articles[10:20]))
        page_1 = paginator.page(
            value=page_2[0].date_unique,
            move_to=inf_paginator.PREV_PAGE)
        self.assertListEqual(list(page_1), list(articles[:10]))

    def test_paginator_next_desc(self):
        articles = Article.objects.all().order_by("-date_unique")
        paginator = SeekPaginator(
            Article.objects.all(), per_page=10, lookup_field="-date_unique")
        page_1 = paginator.page(value=None)
        self.assertListEqual(list(page_1), list(articles[:10]))
        page_2 = paginator.page(value=page_1[-1].date_unique)
        self.assertListEqual(list(page_2), list(articles[10:20]))
        page_3 = paginator.page(value=page_2[-1].date_unique)
        self.assertListEqual(list(page_3), list(articles[20:]))

    def test_paginator_prev_asc(self):
        articles = Article.objects.all().order_by("date_unique")
        paginator = SeekPaginator(
            Article.objects.all(), per_page=10, lookup_field="date_unique")
        page_2 = paginator.page(
            value=list(articles)[20].date_unique,
            move_to=inf_paginator.PREV_PAGE)
        self.assertListEqual(list(page_2), list(articles[10:20]))
        page_1 = paginator.page(
            value=page_2[0].date_unique,
            move_to=inf_paginator.PREV_PAGE)
        self.assertListEqual(list(page_1), list(articles[:10]))

    def test_paginator_next_asc(self):
        articles = Article.objects.all().order_by("date_unique")
        paginator = SeekPaginator(
            Article.objects.all(), per_page=10, lookup_field="date_unique")
        page_1 = paginator.page(value=None)
        self.assertListEqual(list(page_1), list(articles[:10]))
        page_2 = paginator.page(value=page_1[-1].date_unique)
        self.assertListEqual(list(page_2), list(articles[10:20]))
        page_3 = paginator.page(value=page_2[-1].date_unique)
        self.assertListEqual(list(page_3), list(articles[20:]))

    def test_paginator_prev_desc_non_unique(self):
        articles = Article.objects.all().order_by("-date", "-pk")
        paginator = SeekPaginator(
            Article.objects.all(), per_page=10, lookup_field="-date")
        page_2 = paginator.page(
            value=list(articles)[20].date,
            pk=list(articles)[20].pk,
            move_to=inf_paginator.PREV_PAGE)
        self.assertListEqual(list(page_2), list(articles[10:20]))
        page_1 = paginator.page(
            value=page_2[0].date,
            pk=page_2[0].pk,
            move_to=inf_paginator.PREV_PAGE)
        self.assertListEqual(list(page_1), list(articles[:10]))

    def test_paginator_next_desc_non_unique(self):
        articles = Article.objects.all().order_by("-date", "-pk")
        paginator = SeekPaginator(
            Article.objects.all(), per_page=10, lookup_field="-date")
        page_1 = paginator.page(value=None, pk=None)
        self.assertListEqual(list(page_1), list(articles[:10]))
        page_2 = paginator.page(value=page_1[-1].date, pk=page_1[-1].pk)
        self.assertListEqual(list(page_2), list(articles[10:20]))
        page_3 = paginator.page(value=page_2[-1].date, pk=page_2[-1].pk)
        self.assertListEqual(list(page_3), list(articles[20:]))

    def test_paginator_prev_asc_non_unique(self):
        articles = Article.objects.all().order_by("-date", "-pk")
        paginator = SeekPaginator(
            Article.objects.all(), per_page=10, lookup_field="-date")
        page_2 = paginator.page(
            value=list(articles)[20].date,
            pk=list(articles)[20].pk,
            move_to=inf_paginator.PREV_PAGE)
        self.assertListEqual(list(page_2), list(articles[10:20]))
        page_1 = paginator.page(
            value=page_2[0].date,
            pk=page_2[0].pk,
            move_to=inf_paginator.PREV_PAGE)
        self.assertListEqual(list(page_1), list(articles[:10]))

    def test_paginator_next_asc_non_unique(self):
        articles = Article.objects.all().order_by("-date", "-pk")
        paginator = SeekPaginator(
            Article.objects.all(), per_page=10, lookup_field="-date")
        page_1 = paginator.page(value=None, pk=None)
        self.assertListEqual(list(page_1), list(articles[:10]))
        page_2 = paginator.page(value=page_1[-1].date, pk=page_1[-1].pk)
        self.assertListEqual(list(page_2), list(articles[10:20]))
        page_3 = paginator.page(value=page_2[-1].date, pk=page_2[-1].pk)
        self.assertListEqual(list(page_3), list(articles[20:]))

    def test_reverse_date_for_pk(self):
        """
        When the date increment does not match the pk increment,
        we should still get the right results.
        """
        Article.objects.all().delete()
        self.assertFalse(list(Article.objects.all()))

        # asc order date and desc order pk
        date = timezone.now()
        dates = reversed(
            [date + datetime.timedelta(seconds=seconds)
             for seconds in range(25)])

        for i, d in enumerate(dates):
            Article.objects.create(title="%s" % i, date=date, date_unique=d)

        articles = Article.objects.all().order_by("-date_unique")
        paginator = SeekPaginator(
            Article.objects.all(), per_page=10, lookup_field="-date_unique")
        page_1 = paginator.page(value=None)
        self.assertListEqual(list(page_1), list(articles[:10]))
        page_2 = paginator.page(value=page_1[-1].date_unique, pk=page_1[-1].pk)
        self.assertListEqual(list(page_2), list(articles[10:20]))
        page_3 = paginator.page(value=page_2[-1].date_unique, pk=page_2[-1].pk)
        self.assertListEqual(list(page_3), list(articles[20:]))


class PageTest(TestCase):

    def setUp(self):
        date = timezone.now()

        for i in range(25):
            seconds = datetime.timedelta(seconds=i)
            Article.objects.create(title="%s" % i, date=date, date_unique=date + seconds)

    def test_next_page(self):
        articles = Article.objects.all().order_by("date_unique")
        paginator = SeekPaginator(
            Article.objects.all(), per_page=10, lookup_field="date_unique")
        page = paginator.page(value=None)
        self.assertListEqual(list(page), list(articles[:10]))
        page = paginator.page(**page.next_page())
        self.assertListEqual(list(page), list(articles[10:20]))
        page = paginator.page(**page.next_page())
        self.assertListEqual(list(page), list(articles[20:]))

    def test_prev_page(self):
        articles = Article.objects.all().order_by("-date_unique")
        paginator = SeekPaginator(
            Article.objects.all(), per_page=10, lookup_field="-date_unique")
        page = paginator.page(
            value=list(articles)[20].date_unique,
            move_to=inf_paginator.PREV_PAGE)
        self.assertListEqual(list(page), list(articles[10:20]))
        page = paginator.page(
            move_to=inf_paginator.PREV_PAGE,
            **page.prev_page())
        self.assertListEqual(list(page), list(articles[:10]))

    def test_next_objects_left(self):
        articles = Article.objects.all().order_by("-date_unique")
        paginator = SeekPaginator(
            Article.objects.all(), per_page=10, lookup_field="-date_unique")
        page = paginator.page(value=None)
        self.assertEqual(
            page.next_objects_left(),
            len(articles[paginator.per_page:]))
        # last page
        page_last = paginator.page(
            value=list(articles)[-paginator.per_page].date_unique)
        self.assertEqual(page_last.next_objects_left(), 0)

    def test_prev_objects_left(self):
        paginator = SeekPaginator(
            Article.objects.all(), per_page=10, lookup_field="-date_unique")
        page = paginator.page(value=None)
        self.assertEqual(page.prev_objects_left(), 0)
        page = paginator.page(**page.next_page())
        self.assertEqual(page.prev_objects_left(), paginator.per_page)
        page = paginator.page(**page.next_page())
        self.assertEqual(page.prev_objects_left(), paginator.per_page * 2)

    def test_next_pages_left(self):
        paginator = SeekPaginator(
            Article.objects.all(), per_page=10, lookup_field="-date_unique")
        page = paginator.page(value=None)
        self.assertEqual(page.next_pages_left(), 2)
        page = paginator.page(**page.next_page())
        self.assertEqual(page.next_pages_left(), 1)
        page = paginator.page(**page.next_page())
        self.assertEqual(page.next_pages_left(), 0)

    def test_prev_pages_left(self):
        paginator = SeekPaginator(
            Article.objects.all(), per_page=10, lookup_field="-date_unique")
        page = paginator.page(value=None)
        self.assertEqual(page.prev_pages_left(), 0)
        page = paginator.page(**page.next_page())
        self.assertEqual(page.prev_pages_left(), 1)
        page = paginator.page(**page.next_page())
        self.assertEqual(page.prev_pages_left(), 2)

    def test_has_next_page(self):
        paginator = SeekPaginator(
            Article.objects.all(), per_page=10, lookup_field="date_unique")
        page = paginator.page(value=None)
        self.assertTrue(page.has_next())
        page = paginator.page(**page.next_page())
        self.assertTrue(page.has_next())
        page = paginator.page(**page.next_page())
        self.assertFalse(page.has_next())

    def test_has_prev_page(self):
        articles = Article.objects.all().order_by("-date_unique")
        paginator = SeekPaginator(
            Article.objects.all(), per_page=10, lookup_field="-date_unique")
        page = paginator.page(
            value=list(articles)[20].date_unique,
            move_to=inf_paginator.PREV_PAGE)
        self.assertTrue(page.has_previous())
        page = paginator.page(
            move_to=inf_paginator.PREV_PAGE,
            **page.prev_page())
        self.assertFalse(page.has_previous())

    def test_empty_first_page(self):
        paginator = SeekPaginator(
            Article.objects.none(), per_page=10, lookup_field="-date_unique")
        page = paginator.page(value=None)
        self.assertFalse(list(page))
        self.assertFalse(page.has_next())
        self.assertFalse(page.has_previous())
        self.assertEqual(page.next_objects_left(), 0)
        self.assertEqual(page.prev_objects_left(), 0)
        self.assertEqual(page.next_pages_left(), 0)
        self.assertEqual(page.next_page(), {})
        self.assertEqual(page.prev_page(), {})


class SerializerTest(TestCase):

    def test_page_key_to_page_key(self):
        dt = datetime.datetime(
            year=2012, month=3, day=9, hour=22,
            minute=30, second=40, microsecond=123123)
        key = serializers.to_page_key(value=dt, pk=1)
        self.assertEqual(key, '1331343040.123123-1')
        page_dt, page_key = serializers.page_key(key)
        self.assertEqual(page_dt, dt)
        self.assertEqual(page_key, '1')

    def test_page_key_to_page_key_tight_api(self):
        dt = datetime.datetime(
            year=2012, month=3, day=9, hour=22,
            minute=30, second=40, microsecond=123123)
        self.assertEqual(
            serializers.to_page_key(
                *serializers.page_key(
                    serializers.to_page_key(value=dt, pk=1))),
            '1331343040.123123-1')
        self.assertEqual(
            serializers.to_page_key(
                *serializers.page_key(
                    serializers.to_page_key(value=None, pk=None))),
            '')

    def test_to_page_key_microseconds(self):
        dt = datetime.datetime(
            year=2012, month=3, day=9, hour=22,
            minute=30, second=40, microsecond=0)
        self.assertEqual(
            serializers.to_page_key(value=dt, pk=1),
            '1331343040.000000-1')

    def test_page_key_microseconds(self):
        dt = datetime.datetime(
            year=2012, month=3, day=9, hour=22,
            minute=30, second=40, microsecond=0)
        self.assertEqual(
            serializers.page_key(
                serializers.to_page_key(value=dt, pk=1)),
            (dt, '1'))


class PaginatorViewTest(TestCase):

    def setUp(self):
        date = timezone.now()

        for i in range(25):
            seconds = datetime.timedelta(seconds=i)
            Article.objects.create(title="%s" % i, date=date, date_unique=date + seconds)

    def test_first_page(self):
        response = self.client.get(
            reverse('pagination-ajax'),
            HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        res = json.loads(response.content.decode('utf-8'))
        articles = Article.objects.all().order_by("-date", "-pk")
        self.assertEqual(
            res['articles'],
            [{'title': a.title, } for a in articles[:20]])

    def test_last_page(self):
        articles = list(Article.objects.all().order_by("-date", "-pk"))
        art = articles[20]
        page = serializers.to_page_key(value=art.date, pk=art.pk)
        response = self.client.get(
            reverse('pagination-ajax') + '?p={}'.format(page),
            HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        res = json.loads(response.content.decode('utf-8'))
        self.assertEqual(
            res['articles'],
            [{'title': a.title} for a in articles[21:]])
