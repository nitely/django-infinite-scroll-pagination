#-*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.db import models


class Article(models.Model):

    title = models.CharField(max_length=75)
    date = models.DateTimeField()
    date_unique = models.DateTimeField(unique=True)
    is_pinned = models.BooleanField(default=False)
    is_sticky = models.BooleanField(default=False)

    def __unicode__(self):
        return self.title
