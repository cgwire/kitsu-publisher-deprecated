#!/usr/bin/env python

import re

from setuptools import setup, find_packages


with open("gazupublisher/__init__.py") as f:
    _version = re.search(r"__version__\s+=\s+\'(.*)\'", f.read()).group(1)


excluded_packages = ["tests"]

install_requirements = [
    "gazu>=0.7.14",
    "qtazu@git+https://github.com/cgwire/qtazu.git#egg=qtazu",
    "qt.py@git+https://github.com/mottosso/Qt.py.git#egg=qt.py",
    "dccutils@git+https://github.com/cgwire/dccutils.git#egg=dccutils",
]

setup(
    name="gazupublisher",
    version=_version,
    packages=find_packages(exclude=excluded_packages),
    description="Application to publish previews to Kitsu from desktop environments",
    author="CGWire",
    author_email="dev@cg-wire.com",
    license="MIT",
    url="http://www.cg-wire.com",
    entry_points={
        "gui_scripts": ["gazupublisher=gazupublisher.__main__:main"],
    },
    install_requires=install_requirements,
    include_package_data=True,
)
