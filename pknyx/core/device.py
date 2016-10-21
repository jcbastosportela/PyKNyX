# -*- coding: utf-8 -*-

""" Python KNX framework

License
=======

 - B{pKNyX} (U{http://www.pknyx.org}) is Copyright:
  - (C) 2013-2015 Frédéric Mantegazza

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

Device (process) management.

Implements
==========

 - B{Device}

Documentation
=============

The Device is the top-level object. It runs as a process. It mainly encapsulates some initialisations.

Usage
=====

@author: Frédéric Mantegazza
@copyright: (C) 2013-2015 Frédéric Mantegazza
@license: GPL
"""

from pknyx.common import config
from pknyx.common.exception import PKNyXValueError
from pknyx.common.frozenDict import FrozenDict
from pknyx.services.logger import logging; logger = logging.getLogger(__name__)
from pknyx.stack.stack import Stack

import time


class DeviceValueError(PKNyXValueError):
    """
    """


class Device(object):
    """ Device class definition.
    """
    def __new__(cls, *args, **kwargs):
        """ Init the class with all available types for this DPT
        """
        self = super(Device, cls).__new__(cls)

        # Retrieve all parents classes, to get all objects defined there
        classes = cls.__mro__ # do we really want that?

        # class objects named B{FB_xxx} are treated as FunctionalBlock and added to the B{_functionalBlocks} dict
        functionalBlocks = {}
        for cls_ in classes:
            for key, value in cls_.__dict__.items():
                if key.startswith("FB_"):
                    logger.debug("Device.__new__(): %s=(%s)" % (key, repr(value)))
                    name = value['name']

                    # Check if already registered
                    if name in functionalBlocks:
                        raise DeviceValueError("duplicated FB (%s)" % name)

                    cls = value["cls"]
                    value_ = dict(value)  # use a copy to let original untouched
                    value_.pop('cls')     # remove 'cls' key from FB_xxx dict
                    functionalBlocks[name] = cls(**value_)

        self._functionalBlocks = FrozenDict(functionalBlocks)

        # class objects named B{LNK_xxx} are treated as links and added to the B{_links} set
        links = set()
        for cls_ in classes:
            for key, value in cls_.__dict__.items():
                if key.startswith("LNK_"):
                    logger.debug("Device.__new__(): %s=(%s)" % (key, repr(value)))

                    link = (value['fb'], value['dp'], value['gad'])  # TODO: add flags
                    if link in links:
                        raise FunctionalBlockValueError("duplicated link (%s)" % link)

                    links.add(link)

        self._links = frozenset(links)

        try:
            self._desc = cls.__dict__["DESC"]
        except KeyError:
            logger.exception("Device.__new__()")
            self._desc = "Device"

        return self

    def __init__(self, ets, individualAddress=None):
        """ Init Device object.
        """
        super(Device, self).__init__(ets)

        self._stack = Stack(individualAddress)

        self.init()

    @property
    def desc(self):
        return self._desc

    @property
    def stack(self):
        return self._stack

    @property
    def fb(self):
        return self._functionalBlocks

    @property
    def lnk(self):
        return self._links

    def init(self):
        """ Additional user init
        """
        pass

    def start(self):
        """ Start device execution
        """
        self._stack.start()

    def stop(self):
        """ Stop device execution
        """
        self._stack.stop()

