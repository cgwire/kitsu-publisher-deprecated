#!/usr/bin/env python

import re
import os

from subprocess import check_call
from setuptools import setup, find_packages
from setuptools.command.install import install

cmdclass = {}


try:
    from pyqt_distutils.build_ui import build_ui

    has_build_ui = True
except ImportError:
    has_build_ui = False


with open("gazupublisher/__init__.py") as f:
    _version = re.search(r"__version__\s+=\s+\'(.*)\'", f.read()).group(1)


if has_build_ui:
    class build_res(build_ui):
        """Build UI, resources and translations."""

        def run(self):
            # build translations
            check_call(['pylupdate5', 'app.pro'])

            lrelease = os.environ.get('LRELEASE_BIN')
            if not lrelease:
                lrelease = 'lrelease'

            check_call([lrelease, 'app.pro'])

            # build UI & resources
            build_ui.run(self)
            import subprocess
            subprocess.call(["lrelease", "app.pro"])

    cmdclass['build_res'] = build_res


class PreInstallCommand(install):
    """
    Pre-installation  : compile the .ts translation files, and only keep
    the resulting .qm binaries
    """
    def run(self):
        install.run(self)
        import subprocess
        subprocess.call(["lrelease", "gazupublisher/resources/translations/*.ts"])
        process = subprocess.Popen("lrelease app.pro", shell=True)
        process.wait()


cmdclass["install"] = PreInstallCommand

install_requirements = [
    "gazu",
    "qtazu@git+https://github.com/LedruRollin/qtazu.git#egg=qtazu",
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
    package_data={'resources': ['translations/*.qm']},
    exclude_package_data={'resources': ['translations/*.ts']},
    include_package_data=True,
)
