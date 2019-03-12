#-*- coding: utf-8 -*-

from __future__ import unicode_literals
import re
import time
from datetime import datetime

from django.core.paginator import InvalidPage

__all__ = [
    'page_key',
    'to_page_key',
    'InvalidPage']

PAGE_RE = re.compile(r'^(?P<value>[0-9]+\.[0-9]+)-(?P<pk>[0-9]+)$')


def page_key(raw_page):
    """
    Parse a raw page value of ``timestamp-pk`` format.
    Return a tuple of (timestamp, pk)

    :raises: ``InvalidPage``
    """
    if not raw_page:
        return None, None
    m = re.match(PAGE_RE, raw_page)
    if m is None:
        raise InvalidPage('Bad key format')
    try:
        timestamp = datetime.fromtimestamp(float(m.group('value')))
    except (OverflowError, ValueError):
        raise InvalidPage('Key out of range')
    return timestamp, m.group('pk')


def to_page_key(value=None, pk=None):
    """Serialize a value and pk to `timestamp-pk`` format"""
    if value is None:
        return ''
    try:
        timestamp = value.timestamp()
    except AttributeError:
        timestamp = time.mktime(value.timetuple())
    return '{}-{}'.format(timestamp, pk)
