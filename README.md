# infinite-scroll-pagination [![Build Status](https://travis-ci.org/nitely/django-infinite-scroll-pagination.png)](https://travis-ci.org/nitely/django-infinite-scroll-pagination) [![Coverage Status](https://coveralls.io/repos/nitely/django-infinite-scroll-pagination/badge.png?branch=master)](https://coveralls.io/r/nitely/django-infinite-scroll-pagination?branch=master)

infinite-scroll-pagination is a Django lib that implements
[the seek method](http://use-the-index-luke.com/sql/partial-results/fetch-next-page)
(AKA Keyset Paging) for scalable pagination.

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
by a range scan in the desired direction

For a full explanation go to
[the seek method](http://use-the-index-luke.com/sql/partial-results/fetch-next-page)

## Requirements

infinite-scroll-pagination requires the following software to be installed:

* Python 2.7, 3.4, 3.5 or 3.6
* Django 1.11 LTS, 2.0 or 2.1

## Django Rest Framework (DRF)

DRF has the built-in `CursorPagination`
that is similar to this lib. Use that instead.

## Usage

This example pages by a `created_at` date field:

```python
# views.py

from infinite_scroll_pagination.paginator import SeekPaginator, EmptyPage


def pagination_ajax(request, pk=None):
    if not request.is_ajax():
        return Http404()

    created_at = None
    if pk is not None:
        # I'm doing an extra query because datetime serialization/deserialization is hard
        created_at = get_object_or_404(Article, pk=pk).created_at

    articles = Article.objects.all()
    paginator = SeekPaginator(articles, per_page=20, lookup_field='-created_at')

    try:
        page = paginator.page(value=created_at, pk=pk)
    except EmptyPage:
        data = {'error': "this page is empty"}
    else:
        data = {
            'articles': [{'title': article.title} for article in page],
            'has_next': page.has_next_page(),
            'next_page': page.next_page()}

    return HttpResponse(json.dumps(data), content_type="application/json")
```

Paging by pk, id or some `unique=True` field:

```python
# views.py

def pagination_ajax(request, pk=None):
    #...

    paginator = SeekPaginator(queryset, per_page=20, lookup_field='pk')
    page = paginator.page(value=pk)

    #...
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

> Note: an index is require for each direction,
  since the query has a `LIMIT`.
  See [indexes-ordering](https://www.postgresql.org/docs/9.3/indexes-ordering.html)

Pass a limit to the following methods,
or use them in places where there won't be
many records, otherwise they get expensive fast:

* ``next_objects_left``
* ``prev_objects_left``
* ``next_pages_left``
* ``prev_pages_left``

## Scroll up/down

# TODO: explain this. Requires implementing page(..., retrieve='prev')

## Contributing

Feel free to check out the source code and submit pull requests.

You may also report any bug or propose new features in the
[issues tracker](https://github.com/nitely/django-infinite-scroll-pagination/issues)

## Copyright / License

MIT
