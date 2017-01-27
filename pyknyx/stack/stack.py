# -*- coding: utf-8 -*-

""" Python KNX framework

License
=======

 - B{PyKNyX} (U{http://www.pyknyx.org}) is Copyright:
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

KNX Stack management

Implements
==========

 - B{Stack}
 - B{StackValueError}

Documentation
=============

Usage
=====

@author: Frédéric Mantegazza
@copyright: (C) 2013-2015 Frédéric Mantegazza
@license: GPL
"""


import time

from pyknyx.common.exception import PyKNyXValueError
from pyknyx.services.logger import logging; logger = logging.getLogger(__name__)
from pyknyx.stack.individualAddress import IndividualAddress
from pyknyx.stack.layer7.a_groupDataService import A_GroupDataService
from pyknyx.stack.layer4.t_groupDataService import T_GroupDataService
from pyknyx.stack.layer3.n_groupDataService import N_GroupDataService
from pyknyx.stack.layer2.l_dataService import L_DataService
from pyknyx.stack.priority import Priority


class StackValueError(PyKNyXValueError):
    """
    """


class Stack(object):
    """ Stack class

    @ivar _agds: Application layer Group Data Service object
    @type _agds: L{A_GroupDataService}

    @ivar _tgds: Transport layer Group Data Service object
    @type _tgds: L{T_GroupDataService}

    @ivar _ngds: Network layer Group Data Service object
    @type _ngds: L{N_GroupDataService}

    @ivar _lds: Transport layer Data Service object
    @type _lds: L{L_DataService}

    """
    def __init__(self, ets, individualAddress=None):
        """

        raise StackValueError:
        """
        super(Stack, self).__init__()
        if not isinstance(individualAddress, IndividualAddress):
            individualAddress = IndividualAddress(individualAddress)

        self._lds = L_DataService(ets, individualAddress=individualAddress)
        self._ngds = N_GroupDataService(self._lds)
        self._tgds = T_GroupDataService(self._ngds)
        self._agds = A_GroupDataService(self._tgds)

    @property
    def agds(self):
        return self._agds

    @property
    def individualAddress(self):
        return self._lds.physAddr

    def start(self):
        """
        Start the stack. All we need to do is to read initial state from the bus.
        """
        logger.trace("Stack.start()")

        time.sleep(0.25)

        # Iterate over Group to find those which need to send a initial read request
        # (depending on GroupObject init flag)
        logger.debug("Stack.start(): initiate a read request for Group having at least one GroupObject with 'init' flag on")
        for group in self._agds.groups.values():
            for listener in group.listeners:
                try:
                    if listener.flags.init:
                        group.read(priority=Priority())
                        time.sleep(0.1)  # avoid bus saturation
                        break
                except AttributeError:
                    logger.exception("Stack.start(): listener does not seem to be a GroupObject")

        logger.debug("Stack.start(): running")

    def stop(self):
        """
        Stop the stack. Nothing to do here; all done by device.stop and ets.stop
        """
        #logger.trace("Stack.stop()")
        logger.debug("Stack.stop(): stopped")

