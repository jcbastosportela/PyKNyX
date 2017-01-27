# -*- coding: utf-8 -*-

""" Python KNX framework

License
=======

 - B{PyKNyX} (U{https://github.com/M-o-a-T/pyknyx}) is Copyright:
  - (C) 2016-2017 Matthias Urlichs
  - © 2016-2017 Matthias Urlichs
  - PyKNyX is a fork of pKNyX
   - © 2013-2015 Frédéric Mantegazza

This program is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation; either version 2 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program; if not, write to the Free Software
Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
or see:

 - U{http://www.gnu.org/licenses/gpl.html}

Module purpose
==============

Packaging

Implements
==========

Documentation
=============

Usage
=====

@author: Frédéric Mantegazza
@copyright: (C) 2013-2015 Frédéric Mantegazza
@license: GPL
"""


try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

from setuptools.command.test import test as TestCommand
import sys

from pyknyx.common import config

py2_req = []
if sys.version_info.major == 2:
    py2_req.append("argparse")

class PyTest(TestCommand):
    user_options = [('pytest-args=', 'a', "Arguments to pass to pytest")]

    def initialize_options(self):
        TestCommand.initialize_options(self)
        self.pytest_args = []

    def run_tests(self):
        #import here, cause outside the eggs aren't loaded
        import pytest
        errno = pytest.main(self.pytest_args)
        sys.exit(errno)

setup(name=config.APP_NAME,
      version=config.APP_VERSION,

      description="Python KNX framework (MoaT version)",
      long_description=open('README.rst').read(),
      url="https://github.com/M-o-a-T/pyknyx",

      author="Matthias Urlichs",
      author_email="matthias@urlichs.de",

      license="GPL",

      maintainer="Matthias Urlichs",
      maintainer_email="matthias@urlichs.de",

      download_url="https://github.com/M-o-a-T/pyknyx",

      packages=["pyknyx",
                "pyknyx.common",
                "pyknyx.core",
                "pyknyx.core.dptXlator",
                "pyknyx.plugins",
                "pyknyx.services",
                "pyknyx.stack",
                "pyknyx.stack.cemi",
                "pyknyx.stack.knxnetip",
                "pyknyx.stack.layer2",
                "pyknyx.stack.layer3",
                "pyknyx.stack.layer4",
                "pyknyx.stack.layer7",
                "pyknyx.stack.transceiver",
                "pyknyx.tools",
                "pyknyx.tools.templates",
                ],

      extras_require={
        'testing': [
            'pytest',
            'pytest-cov',
        ],
      },
      scripts=["pyknyx/scripts/pyknyx-group.py",
               "pyknyx/scripts/pyknyx-admin.py"],

      install_requires=["APScheduler >= 3",
                        "blinker",
                        "six",
                        ]+py2_req,
      tests_require=['pytest','six'],
      cmdclass = {'test': PyTest},
)
