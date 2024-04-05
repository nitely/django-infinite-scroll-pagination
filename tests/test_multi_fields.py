#-*- coding: utf-8 -*-

import datetime
from unittest import skip

from django.test import TestCase
from django.utils import timezone

from .models import Article
from infinite_scroll_pagination.paginator import SeekPaginator
from infinite_scroll_pagination import paginator as inf_paginator


class Paginator2FieldsTest(TestCase):

    def setUp(self):
        date = timezone.now()
        for i in range(25):
            seconds = datetime.timedelta(seconds=i)
            Article.objects.create(
                title="%s" % i, date=date, date_unique=date + seconds)

    def test_next_desc(self):
        articles = Article.objects.all().order_by('-is_pinned', "-date_unique")
        paginator = SeekPaginator(
            Article.objects.all(),
            per_page=10,
            lookup_field=('-is_pinned', '-date_unique'))
        page_1 = paginator.page(value=None)
        self.assertListEqual(list(page_1), list(articles[:10]))
        page_2 = paginator.page(
            value=(page_1[-1].is_pinned, page_1[-1].date_unique))
        self.assertListEqual(list(page_2), list(articles[10:20]))
        page_3 = paginator.page(
            value=(page_2[-1].is_pinned, page_2[-1].date_unique))
        self.assertListEqual(list(page_3), list(articles[20:]))

    def test_next_desc_pinned(self):
        articles = Article.objects.all().order_by('-is_pinned', "-date_unique")
        for a in articles[:5]:
            a.is_pinned = True
            a.save()
        for a in articles[10:15]:
            a.is_pinned = True
            a.save()
        for a in articles[20:]:
            a.is_pinned = True
            a.save()
        paginator = SeekPaginator(
            Article.objects.all(),
            per_page=10,
            lookup_field=('-is_pinned', '-date_unique'))
        page_1 = paginator.page(value=None)
        self.assertListEqual(list(page_1), list(articles[:10]))
        page_2 = paginator.page(
            value=(page_1[-1].is_pinned, page_1[-1].date_unique))
        self.assertListEqual(list(page_2), list(articles[10:20]))
        page_3 = paginator.page(
            value=(page_2[-1].is_pinned, page_2[-1].date_unique))
        self.assertListEqual(list(page_3), list(articles[20:]))

    def test_prev_desc(self):
        articles = Article.objects.all().order_by('-is_pinned', "-date_unique")
        paginator = SeekPaginator(
            Article.objects.all(),
            per_page=10,
            lookup_field=('-is_pinned', '-date_unique'))
        page_2 = paginator.page(
            value=(list(articles)[20].is_pinned, list(articles)[20].date_unique),
            move_to=inf_paginator.PREV_PAGE)
        self.assertListEqual(list(page_2), list(articles[10:20]))
        page_1 = paginator.page(
            value=(page_2[0].is_pinned, page_2[0].date_unique),
            move_to=inf_paginator.PREV_PAGE)
        self.assertListEqual(list(page_1), list(articles[:10]))

    def test_prev_desc_is_pinned(self):
        articles = Article.objects.all().order_by('-is_pinned', "-date_unique")
        for a in articles[:5]:
            a.is_pinned = True
            a.save()
        for a in articles[10:15]:
            a.is_pinned = True
            a.save()
        for a in articles[20:]:
            a.is_pinned = True
            a.save()
        paginator = SeekPaginator(
            Article.objects.all(),
            per_page=10,
            lookup_field=('-is_pinned', '-date_unique'))
        page_2 = paginator.page(
            value=(list(articles)[20].is_pinned, list(articles)[20].date_unique),
            move_to=inf_paginator.PREV_PAGE)
        self.assertListEqual(list(page_2), list(articles[10:20]))
        page_1 = paginator.page(
            value=(page_2[0].is_pinned, page_2[0].date_unique),
            move_to=inf_paginator.PREV_PAGE)
        self.assertListEqual(list(page_1), list(articles[:10]))

    @skip
    def test_next_asc_desc(self):
        articles = Article.objects.all().order_by('is_pinned', "-date_unique")
        for a in articles[:5]:
            a.is_pinned = True
            a.save()
        for a in articles[10:15]:
            a.is_pinned = True
            a.save()
        for a in articles[20:]:
            a.is_pinned = True
            a.save()
        paginator = SeekPaginator(
            Article.objects.all(),
            per_page=10,
            lookup_field=('is_pinned', '-date_unique'))
        page_1 = paginator.page(value=None)
        self.assertListEqual(list(page_1), list(articles[:10]))
        page_2 = paginator.page(
            value=(page_1[-1].is_pinned, page_1[-1].date_unique))
        self.assertListEqual(list(page_2), list(articles[10:20]))
        page_3 = paginator.page(
            value=(page_2[-1].is_pinned, page_2[-1].date_unique))
        self.assertListEqual(list(page_3), list(articles[20:]))

    @skip
    def test_next_desc_asc(self):
        articles = Article.objects.all().order_by('-is_pinned', "date_unique")
        for a in articles[:5]:
            a.is_pinned = True
            a.save()
        for a in articles[10:15]:
            a.is_pinned = True
            a.save()
        for a in articles[20:]:
            a.is_pinned = True
            a.save()
        paginator = SeekPaginator(
            Article.objects.all(),
            per_page=10,
            lookup_field=('-is_pinned', 'date_unique'))
        page_1 = paginator.page(value=None)
        self.assertListEqual(list(page_1), list(articles[:10]))
        page_2 = paginator.page(
            value=(page_1[-1].is_pinned, page_1[-1].date_unique))
        self.assertListEqual(list(page_2), list(articles[10:20]))
        page_3 = paginator.page(
            value=(page_2[-1].is_pinned, page_2[-1].date_unique))
        self.assertListEqual(list(page_3), list(articles[20:]))

    @skip
    def test_prev_asc_desc(self):
        articles = Article.objects.all().order_by('is_pinned', "-date_unique")
        for a in articles[:5]:
            a.is_pinned = True
            a.save()
        for a in articles[10:15]:
            a.is_pinned = True
            a.save()
        for a in articles[20:]:
            a.is_pinned = True
            a.save()
        paginator = SeekPaginator(
            Article.objects.all(),
            per_page=10,
            lookup_field=('is_pinned', '-date_unique'))
        page_2 = paginator.page(
            value=(list(articles)[20].is_pinned, list(articles)[20].date_unique),
            move_to=inf_paginator.PREV_PAGE)
        self.assertListEqual(list(page_2), list(articles[10:20]))
        page_1 = paginator.page(
            value=(page_2[0].is_pinned, page_2[0].date_unique),
            move_to=inf_paginator.PREV_PAGE)
        self.assertListEqual(list(page_1), list(articles[:10]))

    @skip
    def test_prev_desc_asc(self):
        articles = Article.objects.all().order_by('-is_pinned', "date_unique")
        for a in articles[:5]:
            a.is_pinned = True
            a.save()
        for a in articles[10:15]:
            a.is_pinned = True
            a.save()
        for a in articles[20:]:
            a.is_pinned = True
            a.save()
        paginator = SeekPaginator(
            Article.objects.all(),
            per_page=10,
            lookup_field=('-is_pinned', 'date_unique'))
        page_2 = paginator.page(
            value=(list(articles)[20].is_pinned, list(articles)[20].date_unique),
            move_to=inf_paginator.PREV_PAGE)
        self.assertListEqual(list(page_2), list(articles[10:20]))
        page_1 = paginator.page(
            value=(page_2[0].is_pinned, page_2[0].date_unique),
            move_to=inf_paginator.PREV_PAGE)
        self.assertListEqual(list(page_1), list(articles[:10]))

    def test_next_desc_non_unique(self):
        articles = Article.objects.all().order_by('-is_pinned', "-date", "-pk")
        paginator = SeekPaginator(
            Article.objects.all(),
            per_page=10,
            lookup_field=('-is_pinned', '-date'))
        page_1 = paginator.page(value=None, pk=None)
        self.assertListEqual(list(page_1), list(articles[:10]))
        page_2 = paginator.page(
            value=(page_1[-1].is_pinned, page_1[-1].date),
            pk=page_1[-1].pk)
        self.assertListEqual(list(page_2), list(articles[10:20]))
        page_3 = paginator.page(
            value=(page_2[-1].is_pinned, page_2[-1].date),
            pk=page_2[-1].pk)
        self.assertListEqual(list(page_3), list(articles[20:]))

    def test_next_desc_non_unique_pinned(self):
        articles = Article.objects.all().order_by('-is_pinned', "-date", "-pk")
        for a in articles[:5]:
            a.is_pinned = True
            a.save()
        for a in articles[10:15]:
            a.is_pinned = True
            a.save()
        for a in articles[20:]:
            a.is_pinned = True
            a.save()
        paginator = SeekPaginator(
            Article.objects.all(),
            per_page=10,
            lookup_field=('-is_pinned', '-date'))
        page_1 = paginator.page(value=None, pk=None)
        self.assertListEqual(list(page_1), list(articles[:10]))
        page_2 = paginator.page(
            value=(page_1[-1].is_pinned, page_1[-1].date),
            pk=page_1[-1].pk)
        self.assertListEqual(list(page_2), list(articles[10:20]))
        page_3 = paginator.page(
            value=(page_2[-1].is_pinned, page_2[-1].date),
            pk=page_2[-1].pk)
        self.assertListEqual(list(page_3), list(articles[20:]))

    def test_prev_desc_non_unique(self):
        articles = Article.objects.all().order_by('-is_pinned', "-date", "-pk")
        paginator = SeekPaginator(
            Article.objects.all(),
            per_page=10,
            lookup_field=('-is_pinned', '-date'))
        page_2 = paginator.page(
            value=(list(articles)[20].is_pinned, list(articles)[20].date),
            pk=list(articles)[20].pk,
            move_to=inf_paginator.PREV_PAGE)
        self.assertListEqual(list(page_2), list(articles[10:20]))
        page_1 = paginator.page(
            value=(page_2[0].is_pinned, page_2[0].date),
            pk=page_2[0].pk,
            move_to=inf_paginator.PREV_PAGE)
        self.assertListEqual(list(page_1), list(articles[:10]))

    def test_prev_desc_non_unique_is_pinned(self):
        articles = Article.objects.all().order_by('-is_pinned', "-date", "-pk")
        for a in articles[:5]:
            a.is_pinned = True
            a.save()
        for a in articles[10:15]:
            a.is_pinned = True
            a.save()
        for a in articles[20:]:
            a.is_pinned = True
            a.save()
        paginator = SeekPaginator(
            Article.objects.all(),
            per_page=10,
            lookup_field=('-is_pinned', '-date'))
        page_2 = paginator.page(
            value=(list(articles)[20].is_pinned, list(articles)[20].date),
            pk=list(articles)[20].pk,
            move_to=inf_paginator.PREV_PAGE)
        self.assertListEqual(list(page_2), list(articles[10:20]))
        page_1 = paginator.page(
            value=(page_2[0].is_pinned, page_2[0].date),
            pk=page_2[0].pk,
            move_to=inf_paginator.PREV_PAGE)
        self.assertListEqual(list(page_1), list(articles[:10]))

    @skip
    def test_next_asc_desc_non_unique(self):
        articles = Article.objects.all().order_by('is_pinned', "-date", "-pk")
        for a in articles[:5]:
            a.is_pinned = True
            a.save()
        for a in articles[10:15]:
            a.is_pinned = True
            a.save()
        for a in articles[20:]:
            a.is_pinned = True
            a.save()
        paginator = SeekPaginator(
            Article.objects.all(),
            per_page=10,
            lookup_field=('is_pinned', '-date'))
        page_1 = paginator.page(value=None, pk=None)
        self.assertListEqual(list(page_1), list(articles[:10]))
        page_2 = paginator.page(
            value=(page_1[-1].is_pinned, page_1[-1].date),
            pk=page_1[-1].pk)
        self.assertListEqual(list(page_2), list(articles[10:20]))
        page_3 = paginator.page(
            value=(page_2[-1].is_pinned, page_2[-1].date),
            pk=page_2[-1].pk)
        self.assertListEqual(list(page_3), list(articles[20:]))

    @skip
    def test_next_desc_asc_non_unique(self):
        articles = Article.objects.all().order_by('-is_pinned', "date", "pk")
        for a in articles[:5]:
            a.is_pinned = True
            a.save()
        for a in articles[10:15]:
            a.is_pinned = True
            a.save()
        for a in articles[20:]:
            a.is_pinned = True
            a.save()
        paginator = SeekPaginator(
            Article.objects.all(),
            per_page=10,
            lookup_field=('-is_pinned', 'date'))
        page_1 = paginator.page(value=None, pk=None)
        self.assertListEqual(list(page_1), list(articles[:10]))
        page_2 = paginator.page(
            value=(page_1[-1].is_pinned, page_1[-1].date),
            pk=page_1[-1].pk)
        self.assertListEqual(list(page_2), list(articles[10:20]))
        page_3 = paginator.page(
            value=(page_2[-1].is_pinned, page_2[-1].date),
            pk=page_2[-1].pk)
        self.assertListEqual(list(page_3), list(articles[20:]))

    @skip
    def test_prev_asc_desc_non_unique(self):
        articles = Article.objects.all().order_by('is_pinned', "-date", "-pk")
        for a in articles[:5]:
            a.is_pinned = True
            a.save()
        for a in articles[10:15]:
            a.is_pinned = True
            a.save()
        for a in articles[20:]:
            a.is_pinned = True
            a.save()
        paginator = SeekPaginator(
            Article.objects.all(),
            per_page=10,
            lookup_field=('is_pinned', '-date'))
        page_2 = paginator.page(
            value=(list(articles)[20].is_pinned, list(articles)[20].date),
            pk=list(articles)[20].pk,
            move_to=inf_paginator.PREV_PAGE)
        self.assertListEqual(list(page_2), list(articles[10:20]))
        page_1 = paginator.page(
            value=(page_2[0].is_pinned, page_2[0].date),
            pk=page_2[0].pk,
            move_to=inf_paginator.PREV_PAGE)
        self.assertListEqual(list(page_1), list(articles[:10]))

    @skip
    def test_prev_desc_asc_non_unique(self):
        articles = Article.objects.all().order_by('-is_pinned', "date", "pk")
        for a in articles[:5]:
            a.is_pinned = True
            a.save()
        for a in articles[10:15]:
            a.is_pinned = True
            a.save()
        for a in articles[20:]:
            a.is_pinned = True
            a.save()
        paginator = SeekPaginator(
            Article.objects.all(),
            per_page=10,
            lookup_field=('-is_pinned', 'date'))
        page_2 = paginator.page(
            value=(list(articles)[20].is_pinned, list(articles)[20].date),
            pk=list(articles)[20].pk,
            move_to=inf_paginator.PREV_PAGE)
        self.assertListEqual(list(page_2), list(articles[10:20]))
        page_1 = paginator.page(
            value=(page_2[0].is_pinned, page_2[0].date),
            pk=page_2[0].pk,
            move_to=inf_paginator.PREV_PAGE)
        self.assertListEqual(list(page_1), list(articles[:10]))


class Paginator3FieldsTest(TestCase):

    def setUp(self):
        date = timezone.now()
        for i in range(25):
            seconds = datetime.timedelta(seconds=i)
            Article.objects.create(
                title="%s" % i, date=date, date_unique=date + seconds)

    def test_next_desc(self):
        articles = Article.objects.all().order_by(
            '-is_pinned', '-is_sticky', "-date_unique")
        paginator = SeekPaginator(
            Article.objects.all(),
            per_page=10,
            lookup_field=('-is_pinned', '-is_sticky', '-date_unique'))
        page_1 = paginator.page(value=None)
        self.assertListEqual(list(page_1), list(articles[:10]))
        page_2 = paginator.page(
            value=(page_1[-1].is_pinned, page_1[-1].is_sticky, page_1[-1].date_unique))
        self.assertListEqual(list(page_2), list(articles[10:20]))
        page_3 = paginator.page(
            value=(page_2[-1].is_pinned, page_2[-1].is_sticky, page_2[-1].date_unique))
        self.assertListEqual(list(page_3), list(articles[20:]))

    def test_next_desc_sticky(self):
        articles = Article.objects.all().order_by(
            '-is_pinned', '-is_sticky', "-date_unique")
        for a in articles[:5]:
            a.is_pinned = True
            a.save()
        for a in articles[10:15]:
            a.is_sticky = True
            a.save()
        for a in articles[20:]:
            a.is_pinned = True
            a.save()
        paginator = SeekPaginator(
            Article.objects.all(),
            per_page=10,
            lookup_field=('-is_pinned', '-is_sticky', '-date_unique'))
        page_1 = paginator.page(value=None)
        self.assertListEqual(list(page_1), list(articles[:10]))
        page_2 = paginator.page(
            value=(page_1[-1].is_pinned, page_1[-1].is_sticky, page_1[-1].date_unique))
        self.assertListEqual(list(page_2), list(articles[10:20]))
        page_3 = paginator.page(
            value=(page_2[-1].is_pinned, page_2[-1].is_sticky, page_2[-1].date_unique))
        self.assertListEqual(list(page_3), list(articles[20:]))

    def test_next_desc_sticky_pinned(self):
        articles = Article.objects.all().order_by(
            '-is_pinned', '-is_sticky', "-date_unique")
        for a in articles[:5]:
            a.is_pinned = True
            a.save()
        for a in articles[10:15]:
            a.is_pinned = True
            a.is_sticky = True
            a.save()
        for a in articles[20:]:
            a.is_pinned = True
            a.is_sticky = True
            a.save()
        paginator = SeekPaginator(
            Article.objects.all(),
            per_page=10,
            lookup_field=('-is_pinned', '-is_sticky', '-date_unique'))
        page_1 = paginator.page(value=None)
        self.assertListEqual(list(page_1), list(articles[:10]))
        page_2 = paginator.page(
            value=(page_1[-1].is_pinned, page_1[-1].is_sticky, page_1[-1].date_unique))
        self.assertListEqual(list(page_2), list(articles[10:20]))
        page_3 = paginator.page(
            value=(page_2[-1].is_pinned, page_2[-1].is_sticky, page_2[-1].date_unique))
        self.assertListEqual(list(page_3), list(articles[20:]))

    @skip
    def test_next_desc_asc_sticky_pinned(self):
        articles = Article.objects.all().order_by(
            '-is_pinned', 'is_sticky', "-date_unique")
        for a in articles[:5]:
            a.is_pinned = True
            a.save()
        for a in articles[10:15]:
            a.is_pinned = True
            a.is_sticky = True
            a.save()
        for a in articles[20:]:
            a.is_pinned = True
            a.is_sticky = True
            a.save()
        paginator = SeekPaginator(
            Article.objects.all(),
            per_page=10,
            lookup_field=('-is_pinned', 'is_sticky', '-date_unique'))
        page_1 = paginator.page(value=None)
        self.assertListEqual(list(page_1), list(articles[:10]))
        page_2 = paginator.page(
            value=(page_1[-1].is_pinned, page_1[-1].is_sticky, page_1[-1].date_unique))
        self.assertListEqual(list(page_2), list(articles[10:20]))
        page_3 = paginator.page(
            value=(page_2[-1].is_pinned, page_2[-1].is_sticky, page_2[-1].date_unique))
        self.assertListEqual(list(page_3), list(articles[20:]))

    def test_prev_desc(self):
        articles = Article.objects.all().order_by(
            '-is_pinned', '-is_sticky', "-date_unique")
        paginator = SeekPaginator(
            Article.objects.all(),
            per_page=10,
            lookup_field=('-is_pinned', '-is_sticky', '-date_unique'))
        page_2 = paginator.page(
            value=(
                list(articles)[20].is_pinned,
                list(articles)[20].is_sticky,
                list(articles)[20].date_unique),
            move_to=inf_paginator.PREV_PAGE)
        self.assertListEqual(list(page_2), list(articles[10:20]))
        page_1 = paginator.page(
            value=(
                page_2[0].is_pinned,
                page_2[0].is_sticky,
                page_2[0].date_unique),
            move_to=inf_paginator.PREV_PAGE)
        self.assertListEqual(list(page_1), list(articles[:10]))

    def test_prev_desc_sticky(self):
        articles = Article.objects.all().order_by(
            '-is_pinned', '-is_sticky', "-date_unique")
        for a in articles[:5]:
            a.is_pinned = True
            a.save()
        for a in articles[10:15]:
            a.is_sticky = True
            a.save()
        for a in articles[20:]:
            a.is_pinned = True
            a.save()
        paginator = SeekPaginator(
            Article.objects.all(),
            per_page=10,
            lookup_field=('-is_pinned', '-is_sticky', '-date_unique'))
        page_2 = paginator.page(
            value=(
                list(articles)[20].is_pinned,
                list(articles)[20].is_sticky,
                list(articles)[20].date_unique),
            move_to=inf_paginator.PREV_PAGE)
        self.assertListEqual(list(page_2), list(articles[10:20]))
        page_1 = paginator.page(
            value=(
                page_2[0].is_pinned,
                page_2[0].is_sticky,
                page_2[0].date_unique),
            move_to=inf_paginator.PREV_PAGE)
        self.assertListEqual(list(page_1), list(articles[:10]))

    def test_prev_desc_sticky_pinned(self):
        articles = Article.objects.all().order_by(
            '-is_pinned', '-is_sticky', "-date_unique")
        for a in articles[:5]:
            a.is_pinned = True
            a.save()
        for a in articles[10:15]:
            a.is_pinned = True
            a.is_sticky = True
            a.save()
        for a in articles[20:]:
            a.is_pinned = True
            a.is_sticky = True
            a.save()
        paginator = SeekPaginator(
            Article.objects.all(),
            per_page=10,
            lookup_field=('-is_pinned', '-is_sticky', '-date_unique'))
        page_2 = paginator.page(
            value=(
                list(articles)[20].is_pinned,
                list(articles)[20].is_sticky,
                list(articles)[20].date_unique),
            move_to=inf_paginator.PREV_PAGE)
        self.assertListEqual(list(page_2), list(articles[10:20]))
        page_1 = paginator.page(
            value=(
                page_2[0].is_pinned,
                page_2[0].is_sticky,
                page_2[0].date_unique),
            move_to=inf_paginator.PREV_PAGE)
        self.assertListEqual(list(page_1), list(articles[:10]))

    @skip
    def test_prev_desc_asc_sticky_pinned(self):
        articles = Article.objects.all().order_by(
            '-is_pinned', 'is_sticky', "-date_unique")
        for a in articles[:5]:
            a.is_pinned = True
            a.save()
        for a in articles[10:15]:
            a.is_pinned = True
            a.is_sticky = True
            a.save()
        for a in articles[20:]:
            a.is_pinned = True
            a.is_sticky = True
            a.save()
        paginator = SeekPaginator(
            Article.objects.all(),
            per_page=10,
            lookup_field=('-is_pinned', 'is_sticky', '-date_unique'))
        page_2 = paginator.page(
            value=(
                list(articles)[20].is_pinned,
                list(articles)[20].is_sticky,
                list(articles)[20].date_unique),
            move_to=inf_paginator.PREV_PAGE)
        self.assertListEqual(list(page_2), list(articles[10:20]))
        page_1 = paginator.page(
            value=(
                page_2[0].is_pinned,
                page_2[0].is_sticky,
                page_2[0].date_unique),
            move_to=inf_paginator.PREV_PAGE)
        self.assertListEqual(list(page_1), list(articles[:10]))

    def test_next_desc_non_unique(self):
        articles = Article.objects.all().order_by(
            '-is_pinned', '-is_sticky', "-date", "-pk")
        paginator = SeekPaginator(
            Article.objects.all(),
            per_page=10,
            lookup_field=('-is_pinned', '-is_sticky', '-date'))
        page_1 = paginator.page(value=None, pk=None)
        self.assertListEqual(list(page_1), list(articles[:10]))
        page_2 = paginator.page(
            value=(page_1[-1].is_pinned, page_1[-1].is_sticky, page_1[-1].date),
            pk=page_1[-1].pk)
        self.assertListEqual(list(page_2), list(articles[10:20]))
        page_3 = paginator.page(
            value=(page_2[-1].is_pinned, page_2[-1].is_sticky, page_2[-1].date),
            pk=page_2[-1].pk)
        self.assertListEqual(list(page_3), list(articles[20:]))

    def test_next_desc_sticky_non_unique(self):
        articles = Article.objects.all().order_by(
            '-is_pinned', '-is_sticky', "-date", '-pk')
        for a in articles[:5]:
            a.is_pinned = True
            a.save()
        for a in articles[10:15]:
            a.is_sticky = True
            a.save()
        for a in articles[20:]:
            a.is_pinned = True
            a.save()
        paginator = SeekPaginator(
            Article.objects.all(),
            per_page=10,
            lookup_field=('-is_pinned', '-is_sticky', '-date'))
        page_1 = paginator.page(value=None, pk=None)
        self.assertListEqual(list(page_1), list(articles[:10]))
        page_2 = paginator.page(
            value=(page_1[-1].is_pinned, page_1[-1].is_sticky, page_1[-1].date),
            pk=page_1[-1].pk)
        self.assertListEqual(list(page_2), list(articles[10:20]))
        page_3 = paginator.page(
            value=(page_2[-1].is_pinned, page_2[-1].is_sticky, page_2[-1].date),
            pk=page_2[-1].pk)
        self.assertListEqual(list(page_3), list(articles[20:]))

    def test_next_desc_sticky_pinned_non_unique(self):
        articles = Article.objects.all().order_by(
            '-is_pinned', '-is_sticky', "-date", '-pk')
        for a in articles[:5]:
            a.is_pinned = True
            a.save()
        for a in articles[10:15]:
            a.is_pinned = True
            a.is_sticky = True
            a.save()
        for a in articles[20:]:
            a.is_pinned = True
            a.is_sticky = True
            a.save()
        paginator = SeekPaginator(
            Article.objects.all(),
            per_page=10,
            lookup_field=('-is_pinned', '-is_sticky', '-date'))
        page_1 = paginator.page(value=None, pk=None)
        self.assertListEqual(list(page_1), list(articles[:10]))
        page_2 = paginator.page(
            value=(page_1[-1].is_pinned, page_1[-1].is_sticky, page_1[-1].date),
            pk=page_1[-1].pk)
        self.assertListEqual(list(page_2), list(articles[10:20]))
        page_3 = paginator.page(
            value=(page_2[-1].is_pinned, page_2[-1].is_sticky, page_2[-1].date),
            pk=page_2[-1].pk)
        self.assertListEqual(list(page_3), list(articles[20:]))

    @skip
    def test_next_desc_asc_sticky_pinned_non_unique(self):
        articles = Article.objects.all().order_by(
            '-is_pinned', 'is_sticky', "-date", '-pk')
        for a in articles[:5]:
            a.is_pinned = True
            a.save()
        for a in articles[10:15]:
            a.is_pinned = True
            a.is_sticky = True
            a.save()
        for a in articles[20:]:
            a.is_pinned = True
            a.is_sticky = True
            a.save()
        paginator = SeekPaginator(
            Article.objects.all(),
            per_page=10,
            lookup_field=('-is_pinned', 'is_sticky', '-date'))
        page_1 = paginator.page(value=None, pk=None)
        self.assertListEqual(list(page_1), list(articles[:10]))
        page_2 = paginator.page(
            value=(page_1[-1].is_pinned, page_1[-1].is_sticky, page_1[-1].date),
            pk=page_1[-1].pk)
        self.assertListEqual(list(page_2), list(articles[10:20]))
        page_3 = paginator.page(
            value=(page_2[-1].is_pinned, page_2[-1].is_sticky, page_2[-1].date),
            pk=page_2[-1].pk)
        self.assertListEqual(list(page_3), list(articles[20:]))

    def test_prev_desc_non_unique(self):
        articles = Article.objects.all().order_by(
            '-is_pinned', '-is_sticky', "-date", '-pk')
        paginator = SeekPaginator(
            Article.objects.all(),
            per_page=10,
            lookup_field=('-is_pinned', '-is_sticky', '-date'))
        page_2 = paginator.page(
            value=(
                list(articles)[20].is_pinned,
                list(articles)[20].is_sticky,
                list(articles)[20].date),
            pk=list(articles)[20].pk,
            move_to=inf_paginator.PREV_PAGE)
        self.assertListEqual(list(page_2), list(articles[10:20]))
        page_1 = paginator.page(
            value=(
                page_2[0].is_pinned,
                page_2[0].is_sticky,
                page_2[0].date),
            pk=page_2[0].pk,
            move_to=inf_paginator.PREV_PAGE)
        self.assertListEqual(list(page_1), list(articles[:10]))

    def test_prev_desc_sticky_non_unique(self):
        articles = Article.objects.all().order_by(
            '-is_pinned', '-is_sticky', "-date", '-pk')
        for a in articles[:5]:
            a.is_pinned = True
            a.save()
        for a in articles[10:15]:
            a.is_sticky = True
            a.save()
        for a in articles[20:]:
            a.is_pinned = True
            a.save()
        paginator = SeekPaginator(
            Article.objects.all(),
            per_page=10,
            lookup_field=('-is_pinned', '-is_sticky', '-date'))
        page_2 = paginator.page(
            value=(
                list(articles)[20].is_pinned,
                list(articles)[20].is_sticky,
                list(articles)[20].date),
            pk=list(articles)[20].pk,
            move_to=inf_paginator.PREV_PAGE)
        self.assertListEqual(list(page_2), list(articles[10:20]))
        page_1 = paginator.page(
            value=(
                page_2[0].is_pinned,
                page_2[0].is_sticky,
                page_2[0].date),
            pk=page_2[0].pk,
            move_to=inf_paginator.PREV_PAGE)
        self.assertListEqual(list(page_1), list(articles[:10]))

    def test_prev_desc_sticky_pinned_non_unique(self):
        articles = Article.objects.all().order_by(
            '-is_pinned', '-is_sticky', "-date", '-pk')
        for a in articles[:5]:
            a.is_pinned = True
            a.save()
        for a in articles[10:15]:
            a.is_pinned = True
            a.is_sticky = True
            a.save()
        for a in articles[20:]:
            a.is_pinned = True
            a.is_sticky = True
            a.save()
        paginator = SeekPaginator(
            Article.objects.all(),
            per_page=10,
            lookup_field=('-is_pinned', '-is_sticky', '-date'))
        page_2 = paginator.page(
            value=(
                list(articles)[20].is_pinned,
                list(articles)[20].is_sticky,
                list(articles)[20].date),
            pk=list(articles)[20].pk,
            move_to=inf_paginator.PREV_PAGE)
        self.assertListEqual(list(page_2), list(articles[10:20]))
        page_1 = paginator.page(
            value=(
                page_2[0].is_pinned,
                page_2[0].is_sticky,
                page_2[0].date),
            pk=page_2[0].pk,
            move_to=inf_paginator.PREV_PAGE)
        self.assertListEqual(list(page_1), list(articles[:10]))

    @skip
    def test_prev_desc_asc_sticky_pinned_non_unique(self):
        articles = Article.objects.all().order_by(
            '-is_pinned', 'is_sticky', "-date", '-pk')
        for a in articles[:5]:
            a.is_pinned = True
            a.save()
        for a in articles[10:15]:
            a.is_pinned = True
            a.is_sticky = True
            a.save()
        for a in articles[20:]:
            a.is_pinned = True
            a.is_sticky = True
            a.save()
        paginator = SeekPaginator(
            Article.objects.all(),
            per_page=10,
            lookup_field=('-is_pinned', 'is_sticky', '-date'))
        page_2 = paginator.page(
            value=(
                list(articles)[20].is_pinned,
                list(articles)[20].is_sticky,
                list(articles)[20].date),
            pk=list(articles)[20].pk,
            move_to=inf_paginator.PREV_PAGE)
        self.assertListEqual(list(page_2), list(articles[10:20]))
        page_1 = paginator.page(
            value=(
                page_2[0].is_pinned,
                page_2[0].is_sticky,
                page_2[0].date),
            pk=page_2[0].pk,
            move_to=inf_paginator.PREV_PAGE)
        self.assertListEqual(list(page_1), list(articles[:10]))
