#-*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.core.paginator import EmptyPage, Page


__all__ = ["SeekPaginator", "SeekPage", "EmptyPage"]


class SeekPaginator(object):

    def __init__(self, query_set, per_page, lookup_field):
        self.query_set = query_set
        self.per_page = per_page
        self.lookup_field = lookup_field

    def prepare_order(self):
        lookup_field_desc = "-%s" % self.lookup_field

        if self.lookup_field not in ("pk", "id"):
            return [lookup_field_desc, "-pk"]
        else:
            return [lookup_field_desc, ]

    def prepare_lookup(self, value, pk):
        """
        Lookup:

        ...
        WHERE date <= ?
        AND NOT (date = ? AND id >= ?)
        ORDER BY date DESC, id DESC
        """
        if self.lookup_field not in ("pk", "id"):
            lookup = "%s__lte" % self.lookup_field
            lookup_exclude = {self.lookup_field: value, "pk__gte": pk, }
        else:
            lookup = "%s__lt" % self.lookup_field
            lookup_exclude = None

        lookup_filter = {lookup: value, }
        return lookup_filter, lookup_exclude

    def page(self, value=None, pk=None):
        if (value is None and pk is not None) or (value is not None and pk is None):
            raise ValueError("Both 'value' and 'pk' arguments must be provided")

        query_set = self.query_set

        if value is not None and pk is not None:
            lookup_filter, lookup_exclude = self.prepare_lookup(value, pk)
            query_set = query_set.filter(**lookup_filter)

            if lookup_exclude:
                query_set = query_set.exclude(**lookup_exclude)

        order = self.prepare_order()
        query_set = query_set.order_by(*order)[:self.per_page + 1]

        object_list = list(query_set)
        has_next = len(object_list) > self.per_page
        object_list = object_list[:self.per_page]

        if not object_list and value:
            raise EmptyPage("That page contains no results")

        return SeekPage(object_list=object_list, number=value, paginator=self, has_next=has_next)


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