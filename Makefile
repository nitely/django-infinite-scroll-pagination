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

.PHONY: clean docs test sdist release
