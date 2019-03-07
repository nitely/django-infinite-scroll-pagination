1.0.0
==================

* Adds support for Django 1.11, 2.0 and 2.1.
  No changes were required to support these
* For those upgrading from 0.x, there are
  some backward incompatible changes.
  The following changes are required
  to get the old behaviour:

  * Replace ``lookup_field='myfield'`` in ``SeekPaginator`` by
    ``lookup_field='-myfield'``. This is because prefixing the field
    by ``-`` makes the query in DESC order, instead of ASC.
  * Replace ``page.next_page_pk()`` call by ``page.next_page()['pk']``.
    This is because ``page.next_page_pk()`` was removed, and the new
    method returns a dict of ``{'myfield': ..., 'pk': ...}``

0.2.0
==================

* Drops support for Django 1.5, 1.6 and 1.7
* Adds support for Django 1.8, 1.9 and 1.10
