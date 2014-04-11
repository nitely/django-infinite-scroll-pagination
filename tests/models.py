#-*- coding: utf-8 -*-

from django.db import models


class Article(models.Model):

    title = models.CharField(max_length=75)
    date = models.DateTimeField()
    date_unique = models.DateTimeField(unique=True)

    def __unicode__(self):
        return self.title