# -*- coding: utf-8 -*-

""" Python KNX framework.

License
=======

 - B{PyKNyX} (U{https://github.com/knxd/pyknyx}) is Copyright:
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

Global configuration

@author: Frédéric Mantegazza
@copyright: (C) 2013-2015 Frédéric Mantegazza
@license: GPL
"""

import sys
import os.path


# Name
APP_NAME = "PyKNyX knxd"
APP_VERSION = "2.0.0.dev.1"

# Logger
LOGGER_STREAM_FORMAT = "%(threadName)s::%(message)s"
LOGGER_FILE_FORMAT = "%(asctime)s::%(threadName)s::%(levelname)s::%(message)s"
LOGGER_LEVEL = "DEBUG"
LOGGER_DIR = "/tmp"
LOGGER_MAX_BYTES = 4096 * 1024
LOGGER_BACKUP_COUNT = 4  # set to 0 to disable logging on file
