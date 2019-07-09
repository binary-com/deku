# -*- coding: utf-8 -*-

# Learn more: https://github.com/kennethreitz/setup.py

from setuptools import setup, find_packages


with open('README.md') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

setup(
    name='deku',
    version='0.1.0',
    description='Python service for seamless rolling updates of docker services',
    long_description=readme,
    author='Apoorv Joshi',
    author_email='me@apoorv.space',
    url='https://github.com/4p00rv/deku',
    license=license,
    packages=find_packages(exclude=('tests', 'docs'))
)

