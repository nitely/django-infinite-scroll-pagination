#-*- coding: utf-8 -*-

import datetime
import json

from django.test import TestCase
from django.core.urlresolvers import reverse

from django.utils import timezone

from models import Article
from infinite_scroll_pagination.paginator import SeekPaginator


class PaginatorTest(TestCase):

    def setUp(self):
        date = timezone.now()

        for i in range(25):
            seconds = datetime.timedelta(seconds=i)
            Article.objects.create(title="%s" % i, date=date, date_unique=date + seconds)

        self.paginator = SeekPaginator(Article.objects.all(), per_page=10, lookup_field="date_unique")

    def test_prepare_order(self):
        self.assertListEqual(self.paginator.prepare_order(), ["-date_unique", "-pk"])
        self.paginator.lookup_field = "pk"
        self.assertListEqual(self.paginator.prepare_order(), ["-pk", ])
        self.paginator.lookup_field = "id"
        self.assertListEqual(self.paginator.prepare_order(), ["-id", ])

    def test_prepare_lookup(self):
        lookup_f, lookup_e = self.paginator.prepare_lookup(value=1, pk=2)
        self.assertDictEqual(lookup_f, {"date_unique__lte": 1, })
        self.assertDictEqual(lookup_e, {"date_unique": 1, "pk__gte": 2})

        self.paginator.lookup_field = "pk"
        lookup_f, lookup_e = self.paginator.prepare_lookup(value=2, pk=2)
        self.assertDictEqual(lookup_f, {"pk__lt": 2, })
        self.assertIsNone(lookup_e)

        self.paginator.lookup_field = "id"
        lookup_f, lookup_e = self.paginator.prepare_lookup(value=2, pk=2)
        self.assertDictEqual(lookup_f, {"id__lt": 2, })
        self.assertIsNone(lookup_e)

    def test_paginator(self):
        articles = Article.objects.all().order_by("-date_unique")

        page_1 = self.paginator.page()
        self.assertListEqual(list(page_1), list(articles[:10]))

        page_2 = self.paginator.page(value=page_1[-1].date_unique, pk=page_1[-1].pk)
        self.assertListEqual(list(page_2), list(articles[10:20]))

        page_3 = self.paginator.page(value=page_2[-1].date_unique, pk=page_2[-1].pk)
        self.assertListEqual(list(page_3), list(articles[20:]))

    def test_first_page(self):
        page = self.paginator.page()
        self.assertTrue(page.has_next())

    def test_last_page(self):
        articles = Article.objects.all().order_by("-date_unique")
        next_to_last = list(articles)[-2]

        page = self.paginator.page(value=next_to_last.date_unique, pk=next_to_last.pk)
        self.assertFalse(page.has_next())

    def test_lookup_not_unique(self):
        self.paginator.lookup_field = "date"
        articles = Article.objects.all().order_by("-date", "-pk")

        page_1 = self.paginator.page()
        self.assertListEqual(list(page_1), list(articles[:10]))

        page_2 = self.paginator.page(value=page_1[-1].date, pk=page_1[-1].pk)
        self.assertListEqual(list(page_2), list(articles[10:20]))

    def test_lookup_pk(self):
        self.paginator.lookup_field = "pk"
        articles = Article.objects.all().order_by("-pk")

        page_1 = self.paginator.page()
        self.assertListEqual(list(page_1), list(articles[:10]))

        page_2 = self.paginator.page(value=page_1[-1].pk, pk=page_1[-1].pk)
        self.assertListEqual(list(page_2), list(articles[10:20]))

    def test_lookup_id(self):
        self.paginator.lookup_field = "id"
        articles = Article.objects.all().order_by("-id")

        page_1 = self.paginator.page()
        self.assertListEqual(list(page_1), list(articles[:10]))

        page_2 = self.paginator.page(value=page_1[-1].id, pk=page_1[-1].id)
        self.assertListEqual(list(page_2), list(articles[10:20]))

    def test_reverse_date_for_pk(self):
        """
        When the date increment does not match the pk increment,
        we should still get the right results.
        """
        Article.objects.all().delete()

        # asc order date and desc order pk
        date = timezone.now()
        dates = reversed([date + datetime.timedelta(seconds=seconds)
                          for seconds in range(25)])

        for i, d in enumerate(dates):
            Article.objects.create(title="%s" % i, date=date, date_unique=d)

        articles = Article.objects.all().order_by("-date_unique")

        page_1 = self.paginator.page()
        self.assertListEqual(list(page_1), list(articles[:10]))

        page_2 = self.paginator.page(value=page_1[-1].date_unique, pk=page_1[-1].pk)
        self.assertListEqual(list(page_2), list(articles[10:20]))

        page_3 = self.paginator.page(value=page_2[-1].date_unique, pk=page_2[-1].pk)
        self.assertListEqual(list(page_3), list(articles[20:]))


class PageTest(TestCase):

    def setUp(self):
        date = timezone.now()

        for i in range(25):
            seconds = datetime.timedelta(seconds=i)
            Article.objects.create(title="%s" % i, date=date, date_unique=date + seconds)

        self.paginator = SeekPaginator(Article.objects.all(), per_page=10, lookup_field="date_unique")

    def test_unimplemented(self):
        page = self.paginator.page()
        self.assertRaises(NotImplementedError, page.has_previous)
        self.assertRaises(NotImplementedError, page.next_page_number)
        self.assertRaises(NotImplementedError, page.previous_page_number)
        self.assertRaises(NotImplementedError, page.start_index)
        self.assertRaises(NotImplementedError, page.end_index)

    def test_objects_left(self):
        articles = Article.objects.all().order_by("-date_unique")
        page = self.paginator.page()
        self.assertEqual(page.objects_left, len(articles[self.paginator.per_page:]))

        # last page
        art = list(articles)[-self.paginator.per_page]
        page_last = self.paginator.page(value=art.date_unique, pk=art.pk)
        self.assertEqual(page_last.objects_left, 0)

    def test_pages_left(self):
        page = self.paginator.page()
        self.assertEqual(page.pages_left, 2)

    def test_next_page_pk(self):
        page = self.paginator.page()
        self.assertEqual(page.next_page_pk(), page[-1].pk)


class PaginatorViewTest(TestCase):

    def setUp(self):
        date = timezone.now()

        for i in range(25):
            seconds = datetime.timedelta(seconds=i)
            Article.objects.create(title="%s" % i, date=date, date_unique=date + seconds)

    def test_first_page(self):
        response = self.client.get(reverse('pagination-ajax'),
                                   HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        res = json.loads(response.content)
        articles = Article.objects.all().order_by("-date", "-pk")
        self.assertEqual(res['articles'], [{u'title': a.title, } for a in articles[:20]])

    def test_page(self):
        articles = Article.objects.all().order_by("-date", "-pk")
        art = articles[20]

        response = self.client.get(reverse('pagination-ajax', kwargs={'pk': str(art.pk), }),
                                   HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        res = json.loads(response.content)
        self.assertEqual(res['articles'], [{u'title': a.title, } for a in articles[21:40]])