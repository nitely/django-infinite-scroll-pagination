clean:
	rm -fr dist/ doc/_build/ *.egg-info/

docs:
	cd docs && make clean && make html

test:
	python -Wd runtests.py

sdist: test clean
	python setup.py sdist

release: sdist
	twine upload dist/*

bench_build:
	cd bench && docker-compose build

bench_clean:
	cd bench \
	&& docker-compose stop \
	&& docker-compose rm --force -v

bench_run:
	cd bench \
	&& docker-compose run --rm --entrypoint '/bin/sh -c' paginator '/bin/sh'

.PHONY: clean docs test sdist release
