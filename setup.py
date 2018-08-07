#!/usr/bin/env python
from setuptools import setup, find_packages

setup(
    name='elasticsearch_statsd',

    version='1.0.0',

    install_requires=[
        'elasticsearch',
        'datadog'
    ],

    py_modules=['elasticsearch_statsd']
)
