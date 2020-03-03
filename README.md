# infinite-scroll-pagination

[![Build Status](https://img.shields.io/travis/nitely/django-infinite-scroll-pagination/master.svg?style=flat-square)](https://travis-ci.org/nitely/django-infinite-scroll-pagination)
[![Coverage Status](https://img.shields.io/coveralls/nitely/django-infinite-scroll-pagination/master.svg?style=flat-square)](https://coveralls.io/r/nitely/django-infinite-scroll-pagination)
[![pypi](https://img.shields.io/pypi/v/django-infinite-scroll-pagination.svg?style=flat-square)](https://pypi.python.org/pypi/django-infinite-scroll-pagination)
[![licence](https://img.shields.io/pypi/l/django-infinite-scroll-pagination.svg?style=flat-square)](https://raw.githubusercontent.com/nitely/django-infinite-scroll-pagination/master/LICENSE)

infinite-scroll-pagination is a Django lib that implements
[the seek method](http://use-the-index-luke.com/sql/partial-results/fetch-next-page)
(AKA Keyset Paging or Cursor Pagination) for scalable pagination.

> Note despite its name, this library can be used as a regular paginator,
  a better name would have been ``seek-paginator``, ``keyset-paginator``,
  ``cursor-paginator`` or ``offset-less-paginator`` but it's too late for that now, haha :D

## How it works

Keyset driven paging relies on remembering the top and bottom keys of
the last displayed page, and requesting the next or previous set of rows,
based on the top/last keyset

This approach has two main advantages over the *OFFSET/LIMIT* approach:

* is correct: unlike the *offset/limit* based approach it correctly handles
new entries and deleted entries. Last row of Page 4 does not show up as first
row of Page 5 just because row 23 on Page 2 was deleted in the meantime.
Nor do rows mysteriously vanish between pages. These anomalies are common
with the *offset/limit* based approach, but the *keyset* based solution does
a much better job at avoiding them.
* is fast: all operations can be solved with a fast row positioning followed
by a range scan in the desired direction.

For a full explanation go to
[the seek method](http://use-the-index-luke.com/sql/partial-results/fetch-next-page)

## Requirements

infinite-scroll-pagination requires the following software to be installed:

* Python 3.5, 3.6, 3.7, or 3.8
* Django 2.2 LTS, or 3.0

## Install

```
pip install django-infinite-scroll-pagination
```

## Django Rest Framework (DRF)

DRF has the built-in `CursorPagination`
that is similar to this lib. Use that instead.

## Usage

This example paginates by a `created_at` date field:

```python
# views.py

import json

from django.http import Http404, HttpResponse

from infinite_scroll_pagination import paginator
from infinite_scroll_pagination import serializers

from .models import Article


def pagination_ajax(request):
    if not request.is_ajax():
        return Http404()

    try:
        value, pk = serializers.page_key(request.GET.get('p', ''))
    except serializers.InvalidPage:
        return Http404()

    try:
        page = paginator.paginate(
            query_set=Article.objects.all(),
            lookup_field='-created_at',
            value=value,
            pk=pk,
            per_page=20,
            move_to=paginator.NEXT_PAGE)
    except paginator.EmptyPage:
        data = {'error': "this page is empty"}
    else:
        data = {
            'articles': [{'title': article.title} for article in page],
            'has_next': page.has_next(),
            'has_prev': page.has_previous(),
            'next_objects_left': page.next_objects_left(limit=100),
            'prev_objects_left': page.prev_objects_left(limit=100),
            'next_pages_left': page.next_pages_left(limit=100),
            'prev_pages_left': page.prev_pages_left(limit=100),
            'next_page': serializers.to_page_key(**page.next_page()),
            'prev_page': serializers.to_page_key(**page.prev_page())}

    return HttpResponse(json.dumps(data), content_type="application/json")
```

Paginating by pk, id or some `unique=True` field:

```python
page = paginator.paginate(queryset, lookup_field='pk', value=pk, per_page=20)
```

## Items order

DESC order:

```python
page = paginator.paginate(
    # ...,
    lookup_field='-created_at')
```

ASC order:

```python
page = paginator.paginate(
    # ...,
    lookup_field='created_at')
```

## Fetch next or prev page

Prev page:

```python
page = paginator.paginate(
    # ...,
    move_to=paginator.PREV_PAGE)
```

Next page:

```python
page = paginator.paginate(
    # ...,
    move_to=paginator.NEXT_PAGE)
```

## Serializers

Since paginating by a datetime and a pk is so common,
there is a serializers that will convert both values to ``timestamp-pk``,
for example: ``1552349160.099628-5``, this can be later be used
as a query string ``https://.../articles/?p=1552349160.099628-5``.
There is no need to do the conversion client side, the server can send
the next/previous page keyset serialized, as shown in the "Usage" section.

Serialize:

```python
next_page = serializers.to_page_key(**page.next_page())
prev_page = serializers.to_page_key(**page.prev_page())
```

Deserialize:

```python
value, pk = serializers.page_key(request.GET.get('p', ''))
```

## Performance

The model should have an index that covers the paginate query.
The previous example's model would look like this:

```python
class Article(models.Model):
    title = models.CharField(max_length=255)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        indexes = [
            models.Index(fields=['created_at', 'pk'],
            models.Index(fields=['-created_at', '-pk'])]
```

> Note: an index is require for both directions,
  since the query has a `LIMIT`.
  See [indexes-ordering](https://www.postgresql.org/docs/9.3/indexes-ordering.html)

Pass a limit to the following methods,
or use them in places where there won't be
many records, otherwise they get expensive fast:

* ``next_objects_left``
* ``prev_objects_left``
* ``next_pages_left``
* ``prev_pages_left``

## Contributing

Feel free to check out the source code and submit pull requests.

Please, report any bug or propose new features in the
[issues tracker](https://github.com/nitely/django-infinite-scroll-pagination/issues)

## Copyright / License

MIT
