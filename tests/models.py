#-*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.db import models


class Article(models.Model):

    title = models.CharField(max_length=75)
    date = models.DateTimeField()
    date_unique = models.DateTimeField(unique=True)
    is_pinned = models.BooleanField(default=False)
    is_sticky = models.BooleanField(default=False)

    #class Meta:
        # The benchmarks show index are not used, see
        # https://github.com/nitely/django-infinite-scroll-pagination/pull/8
        #indexes = [
        #    models.Index(fields=['is_pinned', 'is_sticky', 'date', 'id']),
        #    models.Index(fields=['-is_pinned', '-is_sticky', '-date', '-id'])]
        #indexes = [
        #    models.Index(fields=['date', 'id']),
        #    models.Index(fields=['-date', '-id'])]

    def __unicode__(self):
        return self.title
