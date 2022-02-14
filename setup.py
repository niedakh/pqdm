#!/usr/bin/env python

"""The setup script."""

from setuptools import setup, find_packages

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = [
    'bounded-pool-executor', 'tqdm', 'typing-extensions'
]

setup(
    author="Piotr Szymański",
    author_email='niedakh@gmail.com',
    python_requires='>=3.6',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
    description="PQDM is a TQDM and concurrent futures wrapper to allow enjoyable paralellization of progress bars.",
    install_requires=requirements,
    license="MIT license",
    long_description=readme + '\n\n' + history,
    long_description_content_type='text/x-rst',
    include_package_data=True,
    keywords='pqdm',
    name='pqdm',
    packages=find_packages(include=['pqdm', 'pqdm.*']),
    url='https://github.com/niedakh/pqdm',
    version='0.2.0',
    zip_safe=False,
)
