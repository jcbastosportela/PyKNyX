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

from pyknyx.common import config
from pyknyx.common.exception import PyKNyXValueError
from pyknyx.common.frozenDict import FrozenDict
from pyknyx.services.logger import logging; logger = logging.getLogger(__name__)
from pyknyx.stack.stack import Stack
from pyknyx.core.functionalBlock import FB

import time


class DeviceValueError(PyKNyXValueError):
    """
    """

class LNK(object):
    """ Link factory
    This class collects arguments for instantiating a link.

    When setting up a device class, you may either use strings to name the
    DataPoint you wish to associate with the address, or refer to the DP
    directly.

    >>> class ReplayFB(FunctionalBlock):
    ...     replay = DP(access="input", dptId="1.011", default="Inactive")
    ...     replay_period = DP(access="input", dptId="7.006", default=1440)  # min (= 24h)
    ...     GO_01 = GO(replay, flags="CRWU", priority="low")
    ...     GO_02 = GO(replay_period, flags="CRWU", priority="low")

    >>> class Replay(Device):
    ...     replay_fb = FB(ReplayFB, desc="replay fb")
    ...     LNK_01 = LNK(fb="replay_fb", dp="replay", gad="1/1/1")
    ...     LNK_02 = LNK(replay_fb.replay_period, gad="1/1/2")

    """

    def __init__(self, dp, gad, fb=None):
        self.dp = dp
        self.gad = gad
        self.fb = fb

    def gen(self, obj):
        """ instantiate the link.
        """
        fb = self.fb
        if isinstance(fb,str):
            fb = obj.fb[fb]
        elif fb is not None:
            for val in obj.fb.values():
                if val._factory is fb:
                    fb = val
                    break
            else:
                raise KeyError("I could not find the FB factory %s on %s",self.fb,obj)

        if isinstance(self.dp,str):
            dp = fb.go[self.dp]
        else:
            dp = self.dp.gen(obj)
        return (dp, self.gad)

    def __id__(self):
        return id(self.gad)+id(self.dp)
            
    def __eq__(self, other):
        return self.gad == other.gad and self.dp == other.dp
        
        

class Link(object):
    def __init__(self, dp,gad):
        self.dp = dp
        self.gad = gad
    
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
        for cls_ in classes[::-1]:
            for key, value in cls_.__dict__.items():
                if key.startswith("FB_") and isinstance(value, dict):
                    assert 'name' in value, value
                    value = FB(**value)
                    key = value.name

                if isinstance(value, FB):
                    if value.name is None:
                        value.name = key
                    value = value.gen(self, key)
                    value._device = self
                    logger.debug("%s: new FB %s: %s", self, repr(key), value)
                    functionalBlocks[key] = value
                elif key in functionalBlocks and value is None:
                    logger.debug("%s: drop FB %s", self, repr(key))
                    del functionalBlocks[key]

        self._functionalBlocks = FrozenDict(functionalBlocks)

        # class objects named B{LNK_xxx} are treated as links and added to the B{_links} set
        links = dict()
        for cls_ in classes[::-1]:
            for key, value in cls_.__dict__.items():
                if key.startswith("LNK_") and isinstance(value, dict):
                    value = LNK(**value)

                if isinstance(value,LNK):
                    value = value.gen(self)
                    logger.debug("%s: new link %s", key, repr(value))
                    links[key] = value
                elif key in links and value is None:
                    del links[key]

        self._links = frozenset(links.values())

        try:
            self._desc = cls.__dict__["DESC"]
        except KeyError:
            logger.exception("Device.__new__()")
            self._desc = "Device"

        return self

    def __init__(self, ets, individualAddress=None):
        """ Init Device object.
        """
        super(Device, self).__init__()

        self._stack = Stack(ets, individualAddress)

        self.init()
        ets.register(self)

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

