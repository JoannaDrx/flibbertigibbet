#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup

with open('README.md') as readme_file:
    readme = readme_file.read()

requirements = [
    'boto3==1.17.1',
    'httplib2==0.19.1'
]

setup(classifiers=[
    'Development Status :: 2 - Pre-Alpha',
    'Intended Audience :: Developers',
    'Natural Language :: English',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.7',
    'Programming Language :: Python :: 3.8',
],
        description="A chatty bot that sends failed AWS Batch jobs notifications and provides "
                    "emotional support.",
        install_requires=requirements,
        long_description=readme + "\n",
        include_package_data=True,
        name='flibbertigibbet',
        url='https://github.com/JoannaDrx/flibbertigibbet',
        version='0.1',
        author='Joanna Dreux',
        author_email='joanna.dreux@gmail.com',
)
