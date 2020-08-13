#!/usr/bin/env python

from setuptools import setup, find_packages

from kitsupublisher.__version__ import __version__


excluded_packages = ["tests"]

install_requirements = [
    "gazu>=0.7.14",
    "qtazu",
    "qt.py",
    "dccutils",
    "pytz"
]

setup(
    name="kitsupublisher",
    version=__version__,
    packages=find_packages(exclude=excluded_packages),
    description="Application to publish previews to Kitsu from desktop environments",
    author="CGWire",
    author_email="dev@cg-wire.com",
    license="MIT",
    url="http://www.cg-wire.com",
    entry_points={
        "gui_scripts": ["kitsupublisher=kitsupublisher.__main__:main"],
    },
    install_requires=install_requirements,
    include_package_data=True,
)
