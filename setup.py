#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup


requirements = [
    'click==6.7',
    'numpy==1.16.2',
    'Pillow==5.4.1',
]

test_requirements = [
    # TODO: put package test requirements here
]

setup(
    name='projector',
    version='0.1.0',
    description="Python cli (backed with C++) to convert 360 images between projection types",
    author="Pierre Dulac",
    author_email='pierre@dulaccc.me',
    url='https://github.com/dulaccc/projector',
    packages=[
        'projector',
    ],
    package_dir={'projector':
                 'projector'},
    entry_points={
        'console_scripts': [
            'projector=projector.cli:main'
        ]
    },
    include_package_data=True,
    install_requires=requirements,
    license="MIT license",
    zip_safe=False,
    keywords='projector',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        "Programming Language :: Python :: 2",
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
    test_suite='tests',
    tests_require=test_requirements
)
