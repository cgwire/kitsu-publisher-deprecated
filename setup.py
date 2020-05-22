#!/usr/bin/env python

import re
import os
from subprocess import check_call
from setuptools import setup, find_packages, Command
from setuptools.command.sdist import sdist


cmdclass = {}


try:
    from pyqt_distutils.build_ui import build_ui

    has_build_ui = True
except ImportError:
    has_build_ui = False

try:
    from sphinx.setup_command import BuildDoc

    cmdclass["build_docs"] = BuildDoc
except ImportError:
    pass


with open("gazupublisher/__init__.py") as f:
    _version = re.search(r"__version__\s+=\s+\'(.*)\'", f.read()).group(1)


class bdist_app(Command):
    """Custom command to build the application. """

    description = "Build the application"
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        self.run_command("build_res")
        check_call(["pyinstaller", "-y", "app.spec"])


cmdclass["bdist_app"] = bdist_app

install_requirements = [
    "gazu",
    "qtazu@git+https://github.com/Colorbleed/qtazu.git#egg=qtazu",
    "qt.py@git+https://github.com/mottosso/Qt.py.git#egg=qt.py",
]

setup(
    name="gazupublisher",
    version=_version,
    packages=find_packages(),
    description="Application to publish previews to Kitsu from desktop environments",
    author="CGWire",
    author_email="dev@cg-wire.com",
    license="MIT",
    url="http://www.cg-wire.com",
    entry_points={
        "gui_scripts": ["gazupublisher=gazupublisher.__main__:main"],
    },
    cmdclass=cmdclass,
    install_requires=install_requirements,
    package_data={'resources': ['*']},
    include_package_data=True,
)
