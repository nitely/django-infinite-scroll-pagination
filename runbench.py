#!/usr/bin/env python
# -*- coding: utf-8 -*-

import datetime

import django
from django.conf import settings
from django.utils import timezone
from django.core.management import call_command


def django_setup():
    settings.configure(
        DATABASES={
            'default': {
                'ENGINE': 'django.db.backends.postgresql_psycopg2',
                'NAME': 'postgres',
                'USER': 'postgres',
                'PASSWORD': 'postgres',
                'HOST': 'database',
                'PORT': '5432',
            }
        },
        INSTALLED_APPS=[
            "tests",
        ],
        ROOT_URLCONF="tests.urls",
        DEBUG=False,
    )
    django.setup()
    call_command('migrate')

#from tests.models import Article
#from infinite_scroll_pagination.paginator import SeekPaginator
#from infinite_scroll_pagination import paginator as inf_paginator

def populate_db():
    from tests.models import Article
    if Article.objects.all().count() > 0:
        print('Some records found; skipping')
        return
    Article.objects.all().delete()
    date = timezone.now()
    # change to range(5) to create 5M records
    for n in range(1):
        articles = []
        for i in range(1_000_000):
            seconds = datetime.timedelta(microseconds=i+1_000_000*n)
            articles.append(Article(
                title="%s" % (i+1_000_000*n), date=date, date_unique=date + seconds))
        Article.objects.bulk_create(articles)


def bench():
    from timeit import default_timer as timer
    from django.core.paginator import Paginator
    from tests.models import Article
    from infinite_scroll_pagination.paginator import SeekPaginator
    articles = Article.objects.all().order_by(
        '-is_pinned', '-is_sticky', "-date", '-pk')
    #'-is_pinned', '-is_sticky',
    for a in articles[:5]:
        a.is_pinned = True
        a.save()
    for a in articles[10:15]:
        a.is_pinned = True
        a.is_sticky = True
        a.save()
    for a in articles[810_000:810_050]:
        a.is_pinned = True
        a.save()
    for a in articles[510_000:510_050]:
        a.is_pinned = True
        a.save()
    for a in articles[910_000:910_050]:
        a.is_sticky = True
        a.save()

    start = timer()
    article1 = list(articles[800_000:800_010])[0]
    #article1 = list(articles[4_000_000:4_000_010])[0]
    end = timer()
    print("Offset/Limit", end - start)

    start = timer()
    paginator = SeekPaginator(
        Article.objects.all(),
        per_page=10,
        lookup_field=('-is_pinned', '-is_sticky', '-date',))
    page = paginator.page(
        value=(
            article1.is_pinned,
            article1.is_sticky,
            article1.date,),
        pk=article1.pk)
    assert list(page)
    end = timer()
    print("Seek Method", end - start)


def start():
    django_setup()
    print('Populating DB')
    populate_db()
    print('Running bench')
    bench()


if __name__ == "__main__":
    start()
