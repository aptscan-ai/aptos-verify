"""Setup.py for the Aptos Verify project."""
# To make sure the CI build is using "upgrade to newer dependencies", which is useful when you want to check
# if the dependencies are still compatible with the latest versions as they seem to break some unrelated
# tests in main, you can modify this file. The modification can be simply modifying this particular comment.
# e.g. you can modify the following number "00001" to something else to trigger it.
from __future__ import annotations
__author__ = "PhongPham"
__copyright__ = "Copyright (C) 2023 PhongPham"
__doc__ = 'https://github.com/aptscan-ai/aptos-verify'
__license__ = "Public Domain"
__version__ = "1.0"

from setuptools import Command, Distribution, find_namespace_packages, setup
from setuptools.command.develop import develop as develop_orig
from setuptools.command.install import install as install_orig
