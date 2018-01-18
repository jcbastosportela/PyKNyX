# -*- coding: utf-8 -*-

""" Python KNX framework

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

API imports.

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

from pyknyx.core.device import Device, LNK
from pyknyx.core.functionalBlock import FunctionalBlock, FB
from pyknyx.core.datapoint import DP
from pyknyx.core.groupObject import GO
from pyknyx.core.ets import ETS
from pyknyx.services.logger import logging

from pyknyx.services.scheduler import Scheduler
from pyknyx.services.notifier import Notifier

from pyknyx.plugins.mail import MUA


# Instanciate some global objects
schedule = Scheduler()
notify = Notifier()
logger = logging.getLogger( __name__ )

# Del unused imported classes
del Scheduler
del Notifier
