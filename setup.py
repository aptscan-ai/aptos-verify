"""Setup.py for the Aptos Verify project."""
# To make sure the CI build is using "upgrade to newer dependencies", which is useful when you want to check
# if the dependencies are still compatible with the latest versions as they seem to break some unrelated
# tests in main, you can modify this file. The modification can be simply modifying this particular comment.
from __future__ import annotations
__author__ = "PhongPham"
__copyright__ = "Copyright (C) 2023 PhongPham"
__doc__ = 'https://github.com/aptscan-ai/aptos-verify'
__license__ = "Public Domain"
__version__ = "1.0.0"

from setuptools import setup, find_packages

with open('README.md', encoding='UTF-8') as f:
    readme = f.read()

setup(
    name='aptos-verify',
    version=__version__,
    description='Command line user export utility',
    long_description=readme,
    author=__author__,
    author_email='phongpham1805@gmail.com',
    packages=find_packages('aptos_verify'),
    package_dir={'': 'aptos_verify'},
    install_requires=[]
)
