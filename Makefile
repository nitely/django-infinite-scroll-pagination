clean:
	rm -fr dist/ doc/_build/ *.egg-info/

docs:
	cd docs && make clean && make html

test:
	python runtests.py

sdist: test clean
	python setup.py sdist

release: test clean
	python setup.py sdist upload

.PHONY: clean docs test sdist release
