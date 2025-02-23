#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import logging

import django
from django.conf import settings
from django.test.runner import DiscoverRunner


if not settings.configured:
    settings.configure(
        DATABASES={
            "default": {
                "ENGINE": "django.db.backends.sqlite3",
            }
        },
        INSTALLED_APPS=[
            "tests",
        ],
        ROOT_URLCONF="tests.urls",
        DEBUG=False,
        SECRET_KEY="qwerty",
    )


def log_warnings():
    logger = logging.getLogger('py.warnings')
    handler = logging.StreamHandler()
    logger.addHandler(handler)


def run_tests():
    test_runner = DiscoverRunner()
    failures = test_runner.run_tests(["tests", ])
    sys.exit(failures)


def start():
    django.setup()
    log_warnings()
    run_tests()


if __name__ == "__main__":
    start()

