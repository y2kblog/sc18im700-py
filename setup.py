# -*- coding: utf-8 -*-
from setuptools import setup, find_packages
import os

# Constants
NAME = 'sc18im700'
VERSION = '1.0.0'
AUTHOR = 'Y2Kb'
AUTHOR_EMAIL = 'info.y2kb@gmail.com'
DESCRIPTION = 'NXP SC18IM700 Library'
LONG_DESCRIPTION = 'NXP SC18IM700 python library'
URL = 'https://gitlab.com/y2kblog/sc18im700-py'


# Functions
def load_requires_from_file(fname):
    if not os.path.exists(fname):
        raise IOError(fname)
    return [pkg.strip() for pkg in open(fname, 'r')]


setup(
    name=NAME,
    version=VERSION,
    author=AUTHOR,
    author_email=AUTHOR_EMAIL,
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    long_description_content_type="text/markdown",
    python_requires=">=3.10",
    url=URL,
    install_requires=load_requires_from_file('./requirements.txt'),
    packages=find_packages(exclude=['tests']),
    classifiers=[
        "Programming Language :: Python :: 3.10",
        "Operating System :: OS Independent",
    ]
)
