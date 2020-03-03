#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from setuptools import setup


URL = 'https://github.com/nitely/django-infinite-scroll-pagination'
README = "For more info, go to: {}".format(URL)

VERSION = __import__('infinite_scroll_pagination').__version__

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='django-infinite-scroll-pagination',
    version=VERSION,
    description=(
        'infinite-scroll-pagination is a Django lib that implements'
        'the *seek method* for scalable pagination.'),
    author='Esteban Castro Borsani',
    author_email='ecastroborsani@gmail.com',
    long_description=README,
    url=URL,
    packages=[
        'infinite_scroll_pagination',
    ],
    include_package_data=True,
    zip_safe=False,
    license='MIT License',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    ],
)
