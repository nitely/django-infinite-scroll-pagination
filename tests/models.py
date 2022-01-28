#-*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.db import models


class Article(models.Model):

    title = models.CharField(max_length=75)
    date = models.DateTimeField()
    date_unique = models.DateTimeField(unique=True)
    is_pinned = models.BooleanField(default=False)
    is_sticky = models.BooleanField(default=False)

    class Meta:
        # This is only used on the "row values" variation
        indexes = [
            models.Index(fields=['is_pinned', 'is_sticky', 'date', 'id']),
            models.Index(fields=['-is_pinned', '-is_sticky', '-date', '-id'])]

    def __unicode__(self):
        return self.title
