# -*- coding: utf-8 -*-
from setuptools import find_packages, setup

from urlchecker import __version__

with open('README.rst', 'r') as f:
    long_description = f.read()

setup(
    name='urlchecker',
    version=__version__,
    author='Vojtěch Oram',
    author_email='vojtech@oram.cz',
    packages=find_packages(exclude=['docs']),
    url='https://github.com/Flaiming/urlchecker',
    license='MIT',
    description='Module for checking is given URLs are working and if so, if they are parking domains or not.',
    long_description=long_description,
    test_suite='nose2.collector.collector',
    install_requires=[
        'requests'
    ],
    zip_safe=False
)
