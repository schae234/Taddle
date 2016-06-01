#!/usr/bin/env python

from setuptools import setup
import io
import os
import re

from setuptools import setup, find_packages, Extension

def read(*names, **kwargs):
    with io.open(
        os.path.join(os.path.dirname(__file__), *names),
        encoding=kwargs.get("encoding", "utf8")
    ) as fp:
        return fp.read()

def find_version(*file_paths):
    version_file = read(*file_paths)
    version_match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]",
                              version_file, re.M)
    if version_match:
        return version_match.group(1)
    raise RuntimeError("Unable to find version string.")

setup(
    name='taddle',
    version=find_version('taddle','__init__.py'),
    packages= find_packages(),
    scripts = [
        'taddle/cli/taddle'    
    ],
    description='Python IP reporter',
    author='Rob Schaefer',
    author_email='rob@linkag.io',
    url='http://linkage.io',
)

