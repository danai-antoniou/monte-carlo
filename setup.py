"""A setuptools based setup module.
See:
https://packaging.python.org/en/latest/distributing.html
https://github.com/pypa/sampleproject
"""

import os
# To use a consistent encoding
from codecs import open
from os import path

# Always prefer setuptools over distutils
from setuptools import setup, find_packages

here = path.abspath(path.dirname(__file__))


# Get a file path using the directory this file is in
def __path(filename):
    return os.path.join(os.path.dirname(__file__), filename)


# The default version if building locally
version = '1.0.999-dev'

""" If this has been built in Jenkins then this file should exist and give the version number.
    We need to do this via file as the env variable will not be present when doing pip install
    using this dependency
"""
if os.path.exists(__path('artifact_version.info')):
    with open(__path('artifact_version.info')) as version_info:
        version = version_info.read().strip()

setup(
    name='monte-carlo',

    # Versions should comply with PEP440.  For a discussion on single-sourcing
    # the version across setup.py and the project code, see
    # https://packaging.python.org/en/latest/single_source_version.html
    version=version,

    description='Monte carlo permutation tests',

    url='https://github.com/danai-antoniou/monte-carlo.git',

    author='Danai Antoniou',
    author_email='antoniou.danai@gmail.com',

    license='Proprietary',

    classifiers=[
        'Development Status :: 4 - Alpha',

        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',

        'License :: Proprietary',

        'Programming Language :: Python :: 3',
    ],

    keywords='experimentation hypothesis testing',

    packages=find_packages(),

    install_requires=['scipy>=1.0.0',
                      'numpy==1.15.4',
                      'matplotlib==3.0.2',
                      ],

)
