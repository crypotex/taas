#!/usr/bin/env python

from setuptools import setup, find_packages


dev_requires = [
    'Sphinx==1.3.1',
]

tests_requires = [
    'factory-boy==2.5.2',
]

install_requires = [
    'Django==1.8.4',
    'django-model-utils==2.3.1',
    'django-widget-tweaks==1.4.1',
]

setup(
    name='taas',
    version='0.1.0',
    author='TAAS Team',
    author_email='taas@gmail.com',
    url='https://github.com/crypotex/taas',
    description='Reservation system for dog agility training ground.',
    long_description=open('README.md').read(),
    packages=find_packages(),
    install_requires=install_requires,
    tests_require=tests_requires,
    test_suite='taas.server.test_runner.run_tests',
    extras_require={
        'dev': dev_requires,
        'tests': tests_requires
    },
    classifiers=[
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License (GPL)',
        'Operating System :: OS Independent',
    ],
)
