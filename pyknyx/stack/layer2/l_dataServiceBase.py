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

Layer2 common code

Implements
==========

 - B{L_DataServiceBase}
 - B{L_DataServiceBroadcast}
 - B{L_DataServiceUnicast}

Documentation
=============

Usage
=====

@author: Frédéric Mantegazza
@copyright: (C) 2013-2015 Frédéric Mantegazza
@license: GPL
"""


from pyknyx.common.exception import PyKNyXValueError
from pyknyx.services.logger import logging; logger = logging.getLogger(__name__)
from pyknyx.stack.individualAddress import IndividualAddress

class NOT_REQUIRED:
    pass

class L_DataServiceBase(object):
    """
    Base class for sending and receiving frames.

    @ivar _ets: main dispatcher.
    @type _ets: ETS<pyknyx.core.ets>

    @ivar _physAddr: set to this device's physical address. Leave at None if
    the transceiver addresses a broadcast medium with more than one device.
    Set to NOT_REQUIRED if the device never sends anything.
    """
    _physAddr = None
    hop = False # instead of isinstance()

    def __init__(self, ets, individualAddress=None):
        """

        """
        super(L_DataServiceBase, self).__init__()

        if self._physAddr is NOT_REQUIRED:
            pass
        else:
            if individualAddress is None:
                individualAddress = ets.allocAddress()
            elif not isinstance(individualAddress,IndividualAddress):
                individualAddress = IndividualAddress(individualAddress)
            self._physAddr = individualAddress

        self._ets = ets
        ets.addLayer2(self)

    @property
    def ets(self):
        return self._ets

    @property
    def physAddr(self):
        return self._physAddr

    def wantsGroupFrame(self, cEMI):
        return True

    def wantsIndividualFrame(self, cEMI, force=False):
        """
        Process a frame addressed to an individual (i.e. physical) address.

        @param force: set to True if no transceiver processed the frame.
        This may happen e.g. when addressing previously-unknown devices.
        """
        return False

    def start(self):
        pass

    def stop(self):
        pass

    def dataInd(self, cEMI):
        """
        Called by ETS to transmit a packet
        """
        raise NotImplementedError

    def dataReq(self, cEMI):
        """
        Called by upper layers to forward a packet
        """
        self._ets.putFrame(self, cEMI)

    def cleanup(self):
        raise NotImplementedError

class L_DataServiceBroadcast(L_DataServiceBase):
    """
    A data service which is attached to a broadcast medium.
    """
    hop = True

    def __init__(self, *args, **kwargs):
        super(L_DataServiceBroadcast, self).__init__(*args, **kwargs)

        self._physAddrs = set()
        self._physAddrs.add(IndividualAddress((7,15,15))) ## programming

    def wantsIndividualFrame(self, cEMI, force=False):
        if not force and cEMI.destinationAddress not in self._physAddrs:
            return False
        return True

    def addAddr(self, addr):
        self._physAddrs.add(self)

class L_DataServiceUnicast(L_DataServiceBase):
    """
    A data service attached to a single device (usually via pyknyx.stack.stack.Stack)
    """
    def wantsIndividualFrame(self, cEMI, force=False):
        if self._physAddr is NOT_REQUIRED or self._physAddr != cEMI.destinationAddress:
            return False
        return True

