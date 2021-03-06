# -*- coding: utf-8 -*-
from setuptools import setup, find_packages

setup(
    name='boa_parser',
    version=0.1,
    packages=find_packages(),
    package_dir={'boa_parser': 'boa_parser'},
    entry_points={'console_scripts': ['boa_parser = boa_parser.main:main']},
    include_package_data=True,
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.4'
    ]
)
