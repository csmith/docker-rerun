"""Setuptools based setup module for docker-rerun."""

from setuptools import setup, find_packages
from os import path

here = path.abspath(path.dirname(__file__))

setup(
    name='docker-rerun',

    version='0.1.1',

    description='Command-line tool to re-run a docker container',
    long_description='docker-rerun is a small utility script that makes it ' \
                     'easy to re-run docker containers using the same ' \
                     'arguments you used previously.' \
                     '\n\n' \
                     'Want to update to a newer image, or add a missing port ' \
                     'publication? docker-rerun’s got you covered.' \
                     '\n\n' \
                     'See the GitHub project_ for more info.' \
                     '\n\n' \
                     '.. _project: https://github.com/csmith/docker-rerun',

    url='https://github.com/csmith/docker-rerun',

    author='Chris Smith',
    author_email='chris87@gmail.com',

    license='MIT',

    # See https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3 :: Only',
        'Topic :: System :: Systems Administration',
        'Topic :: Utilities',
    ],

    keywords='docker container',

    py_modules=["docker_rerun"],

    install_requires=[],

    test_suite='nose.collector',

    extras_require={
        'dev': ['pylint'],
        'test': ['coverage', 'nose', 'python-coveralls'],
    },

    entry_points={
        'console_scripts': [
            'docker-rerun=docker_rerun:entrypoint',
        ],
    },
)

