# infinite-scroll-pagination [![Build Status](https://travis-ci.org/nitely/django-infinite-scroll-pagination.png)](https://travis-ci.org/nitely/django-infinite-scroll-pagination) [![Coverage Status](https://coveralls.io/repos/nitely/django-infinite-scroll-pagination/badge.png?branch=master)](https://coveralls.io/r/nitely/django-infinite-scroll-pagination?branch=master)

infinite-scroll-pagination is a Django app that implements [the seek method](http://use-the-index-luke.com/sql/partial-results/fetch-next-page) (AKA Keyset Paging) for scalable pagination.

## How it works

Keyset driven paging relies on remembering the top and bottom keys of the last displayed page, and requesting the next or previous set of rows, based on the top/last keyset

This approach has two main advantages over the *OFFSET/LIMIT* approach:

* is correct: unlike the *offset/limit* based approach it correctly handles new entries and deleted entries. Last row of Page 4 does not show up as first row of Page 5 just because row 23 on Page 2 was deleted in the meantime. Nor do rows mysteriously vanish between pages. These anomalies are common with the *offset/limit* based approach, but the *keyset* based solution does a much better job at avoiding them.
* is fast: all operations can be solved with a fast row positioning followed by a range scan in the desired direction

For a full explanation go to [the seek method](http://use-the-index-luke.com/sql/partial-results/fetch-next-page)

## Requirements

infinite-scroll-pagination requires the following software to be installed:

* Python 2.7
* Django +1.4 (tested locally on 1.6)

## Configuration

1. None :smile:

## Usage

soon

## Contributing

Feel free to check out the source code and submit pull requests.

You may also report any bug or propose new features in the [issues tracker](https://github.com/nitely/django-infinite-scroll-pagination/issues)

## Copyright / License

Copyright 2014 [Esteban Castro Borsani](https://github.com/nitely).

Licensed under the [MIT License](https://github.com/nitely/django-infinite-scroll-pagination/blob/master/LICENSE).

Unless required by applicable law or agreed to in writing,
software distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and limitations under the License.