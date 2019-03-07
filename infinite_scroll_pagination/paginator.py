#-*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.core.paginator import EmptyPage, Page


__all__ = ["SeekPaginator", "SeekPage", "EmptyPage"]


class SeekPaginator(object):

    def __init__(self, query_set, per_page, lookup_field):
        assert isinstance(lookup_field, str), 'String expected'
        assert isinstance(per_page, int), 'Int expected'
        self.query_set = query_set
        self.per_page = per_page
        self.is_desc = lookup_field.startswith('-')
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

    def prepare_lookup(self, value, pk=None):
        """
        Lookup (-DESC)::

            # ...
            WHERE date <= ?
            AND NOT (date = ? AND id >= ?)
            ORDER BY date DESC, id DESC

        """
        lookup_include = '%s__gt' % self.lookup_field
        lookup_exclude_pk = 'pk__lte'
        if self.is_desc:
            lookup_include = '%s__lt' % self.lookup_field
            lookup_exclude_pk = 'pk__gte'
        lookup_exclude = None
        if pk is not None:
            lookup_include = "%se" % lookup_include
            lookup_exclude = {self.lookup_field: value, lookup_exclude_pk: pk}
        lookup_filter = {lookup_include: value}
        return lookup_filter, lookup_exclude

    def apply_filter(self, query_set, value, pk):
        lookup_filter, lookup_exclude = self.prepare_lookup(value, pk)
        query_set = query_set.filter(**lookup_filter)
        if lookup_exclude:
            query_set = query_set.exclude(**lookup_exclude)
        return query_set

    def page(self, value, pk=None):
        """
        The param ``value`` may be ``None`` on the first page.
        Pass both ``value`` and ``pk`` when the ``lookup_field``'s model
        field is not unique. Otherwise, pass just the ``value``
        """
        query_set = self.query_set
        if value is not None:
            query_set = self.apply_filter(query_set, value, pk)

        query_set = query_set.order_by(
            *self.prepare_order(
                has_pk=pk is not None))[:self.per_page + 1]

        object_list = list(query_set)
        has_next = len(object_list) > self.per_page
        object_list = object_list[:self.per_page]

        if not object_list and value:
            raise EmptyPage("That page contains no results")

        return SeekPage(
            object_list=object_list,
            number=value,
            paginator=self,
            has_next=has_next)


class SeekPage(Page):

    def __init__(self, object_list, number, paginator, has_next):
        super(SeekPage, self).__init__(object_list, number, paginator)
        self._has_next = has_next
        self._objects_left = None
        self._pages_left = None

    def __repr__(self):
        return '<Page value %s>' % self.number or ""

    def has_next(self):
        return self._has_next

    def has_previous(self):
        raise NotImplementedError

    def has_other_pages(self):
        return self.has_next()

    def next_page_number(self):
        raise NotImplementedError

    def previous_page_number(self):
        raise NotImplementedError

    def start_index(self):
        raise NotImplementedError

    def end_index(self):
        raise NotImplementedError

    @property
    def objects_left(self):
        """
        Returns the total number of *objects* left
        """
        if not self.has_next():
            return 0

        if self._objects_left is None:
            last = self.object_list[-1]
            value = getattr(last, self.paginator.lookup_field)
            lookup_filter, lookup_exclude = self.paginator.prepare_lookup(value, last.pk)
            query_set = self.paginator.query_set.filter(**lookup_filter)

            if lookup_exclude:
                query_set = query_set.exclude(**lookup_exclude)

            order = self.paginator.prepare_order()
            self._objects_left = query_set.order_by(*order).count()

        return self._objects_left

    @property
    def pages_left(self):
        """
        Returns the total number of *pages* left
        """
        if not self.objects_left:
            return 0

        if self._pages_left is None:
            self._pages_left = (-self.objects_left // self.paginator.per_page) * -1  # ceil

        return self._pages_left

    def next_page_pk(self):
        return self.object_list[-1].pk
