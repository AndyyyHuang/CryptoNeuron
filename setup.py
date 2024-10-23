# Copyright © 2024 <Andy>


import re
import os
import codecs
import pathlib
from os import path
from io import open
from setuptools import setup, find_packages
from pkg_resources import parse_requirements

from setuptools import setup


def read_requirements(path):
    with open(path, "r") as f:
        requirements = f.read().splitlines()
        processed_requirements = []

        for req in requirements:
            # For git or other VCS links
            if req.startswith("git+") or "@" in req:
                pkg_name = re.search(r"(#egg=)([\w\-_]+)", req)
                if pkg_name:
                    processed_requirements.append(pkg_name.group(2))
                else:
                    # You may decide to raise an exception here,
                    # if you want to ensure every VCS link has an #egg=<package_name> at the end
                    continue
            else:
                processed_requirements.append(req)
        return processed_requirements


requirements = read_requirements("requirements.txt")
here = path.abspath(path.dirname(__file__))

with open(path.join(here, "README.md"), encoding="utf-8") as f:
    long_description = f.read()

# loading version from setup.py
with codecs.open(
    os.path.join(here, "cryptoneurons/__init__.py"), encoding="utf-8"
) as init_file:
    version_match = re.search(
        r"^__version__ = ['\"]([^'\"]*)['\"]", init_file.read(), re.M
    )
    version_string = version_match.group(1)


setup(
    name='CryptoNeuron',
    description='CryptoNeuron',
    version=version_string,
    packages=['cryptoneurons'],
    url="https://github.com/AndyyyHuang/CryptoNeuron",
    author="Andy Huang",
    author_email="",  # TODO(developer): Change this value to your module subnet author email.
    license='MIT',
    python_requires=">=3.8",
    install_requires=requirements,
)