#-*- coding: utf-8 -*-

from __future__ import unicode_literals

import collections.abc

from django.core.paginator import EmptyPage

__all__ = [
    "SeekPaginator",
    "SeekPage",
    "EmptyPage",
    'NEXT_PAGE',
    'PREV_PAGE']


NEXT_PAGE = 1
PREV_PAGE = 2


class SeekPaginator(object):

    def __init__(self, query_set, per_page, lookup_field):
        assert isinstance(lookup_field, str), 'String expected'
        assert isinstance(per_page, int), 'Int expected'
        self.query_set = query_set
        self.per_page = per_page
        self.is_desc = lookup_field.startswith('-')
        self.is_asc = not self.is_desc
        self.lookup_field = lookup_field.lstrip('-')

    def prepare_order(self, has_pk=False):
        pk_sort = 'pk'
        lookup_sort = self.lookup_field
        if self.is_desc:
            pk_sort = '-%s' % pk_sort
            lookup_sort = '-%s' % lookup_sort
        if has_pk:
            return [lookup_sort, pk_sort]
        return [lookup_sort]

    def prepare_lookup(self, value, pk, move_to):
        lookup_include = '%s__gt' % self.lookup_field
        lookup_exclude_pk = 'pk__lte'
        if ((self.is_desc and move_to == NEXT_PAGE) or
                (self.is_asc and move_to == PREV_PAGE)):
            lookup_include = '%s__lt' % self.lookup_field
            lookup_exclude_pk = 'pk__gte'
        lookup_exclude = None
        if pk is not None:
            lookup_include = "%se" % lookup_include
            lookup_exclude = {self.lookup_field: value, lookup_exclude_pk: pk}
        lookup_filter = {lookup_include: value}
        return lookup_filter, lookup_exclude

    def apply_filter(self, value, pk, move_to):
        query_set = self.query_set
        lookup_filter, lookup_exclude = self.prepare_lookup(
            value=value, pk=pk, move_to=move_to)
        query_set = query_set.filter(**lookup_filter)
        if lookup_exclude:
            query_set = query_set.exclude(**lookup_exclude)
        return query_set

    def seek(self, value, pk, move_to):
        """
        Skip the current record in case
        there are multiple with the same value

        Lookup next page (-DESC)::

            # ...
            WHERE date <= ?
            AND NOT (date = ? AND id >= ?)
            ORDER BY date DESC, id DESC

        """
        query_set = self.query_set
        if value is not None:
            query_set = self.apply_filter(
                value=value, pk=pk, move_to=move_to)
        query_set = query_set.order_by(
            *self.prepare_order(has_pk=pk is not None))
        return query_set

    def page(self, value, pk=None, move_to=NEXT_PAGE):
        """
        The param ``value`` may be ``None`` on the first page.
        Pass both ``value`` and ``pk`` when the ``lookup_field``'s model
        field is not unique. Otherwise, pass just the ``value``
        """
        assert move_to in (NEXT_PAGE, PREV_PAGE)
        query_set = self.seek(
            value=value, pk=pk, move_to=move_to)

        if value and not query_set.exists():
            raise EmptyPage()

        return SeekPage(
            query_set=query_set,
            key={'value': value, 'pk': pk},
            paginator=self)


class SeekPage(collections.abc.Sequence):

    def __init__(self, query_set, key, paginator):
        self._query_set = query_set
        self._key = key
        self._object_list = None
        self.paginator = paginator

    def __repr__(self):
        return '<Page value={value} pk={pk}>'.format(**self._key)

    @property
    def object_list(self):
        if self._object_list is not None:
            return self._object_list
        # We could fetch an extra item an
        # save a query on has_prev/next_page,
        # but meh, the query for hax_X should be fairly cheap
        self._object_list = list(self._query_set[:self.paginator.per_page])
        return self._object_list

    def _some_seek(self, direction):
        assert self.object_list
        assert direction in (NEXT_PAGE, PREV_PAGE)
        last = self.object_list[0]
        if direction == NEXT_PAGE:
            last = self.object_list[-1]
        pk = None
        if self._key['pk'] is not None:
            pk = last.pk
        return self.paginator.seek(
            value=getattr(last, self.paginator.lookup_field),
            pk=pk,
            move_to=direction)

    # XXX make it a property as in Page
    def has_next_page(self):
        if not self.object_list:
            return False
        return self._some_seek(NEXT_PAGE).exists()

    def has_prev_page(self):
        if not self.object_list:
            return False
        return self._some_seek(PREV_PAGE).exists()

    def next_objects_left(self, limit=None):
        if not self.object_list:
            return 0
        qs = self._some_seek(NEXT_PAGE)
        if limit:
            qs = qs[:limit]
        return qs.count()

    def prev_objects_left(self, limit=None):
        if not self.object_list:
            return 0
        qs = self._some_seek(PREV_PAGE)
        if limit:
            qs = qs[:limit]
        return qs.count()

    def _some_pages_left(self, direction, limit):
        some_objects_left = self.prev_objects_left
        if direction == NEXT_PAGE:
            some_objects_left = self.next_objects_left
        limit = (limit or 0) * self.paginator.per_page
        return (-some_objects_left(limit) // self.paginator.per_page) * -1  # ceil

    def next_pages_left(self, limit=None):
        return self._some_pages_left(NEXT_PAGE, limit)

    def prev_pages_left(self, limit=None):
        return self._some_pages_left(PREV_PAGE, limit)

    def _some_page(self, index):
        return {
            self.paginator.lookup_field: getattr(
                self.object_list[index], self.paginator.lookup_field),
            'pk': self.object_list[index].pk}

    def next_page(self):
        return self._some_page(-1)

    def prev_page(self):
        return self._some_page(0)
