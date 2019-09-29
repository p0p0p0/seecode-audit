# coding: utf-8

from setuptools import setup, find_packages

from seecode import __version__


setup(
    name='seecode-audit',
    version=__version__,
    description='Distributed white box code scanning tool',
    author='MyKings',
    author_email='xsseroot@gmail.com',
    url='git@github.com:seecode-audit/seecode-audit.git',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'django',
        'mysql-python',
        'requests',
        'redis',
        'pyyaml',
        'netaddr',
        'django-redis',
        'django-cacheops',
    ],
    extras_require={
        'dev': [
            'devpi>=2.1.0',
            'prospector',
            ],
        'test': [
            'coverage>=3.7.1',
            'nose>=1.3.6',
            ],
        'docs': [
            'Sphinx>=1.3.1',
            ],
        'build': [
            'devpi>=2.1.0',
            ],
        },
    test_suite='nose.collector',
    zip_safe=False,
)
