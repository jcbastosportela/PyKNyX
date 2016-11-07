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

Application layer group data management

Implements
==========

 - B{L_DataService}
 - B{L_DSValueError}

Documentation
=============

Usage
=====

@author: Frédéric Mantegazza
@copyright: (C) 2013-2015 Frédéric Mantegazza
@license: GPL
"""


import time
import threading

from pknyx.common.exception import PKNyXValueError
from pknyx.services.logger import logging; logger = logging.getLogger(__name__)
from pknyx.stack.individualAddress import IndividualAddress
from pknyx.stack.priorityQueue import PriorityQueue
from pknyx.stack.layer3.n_groupDataListener import N_GroupDataListener
from pknyx.stack.layer2.l_dataServiceBase import L_DataServiceUnicast, NOT_REQUIRED
from pknyx.stack.cemi.cemiLData import CEMILData

PRIORITY_DISTRIBUTION = (-1, 3, 2, 1)

class L_DSValueError(PKNyXValueError):
    """
    """


class L_DataService(L_DataServiceUnicast):
    """ L_DataService class

    @ivar _individualAddress: own Individual Address
    @type _individualAddress: str or L{IndividualAddress<pknyx.core.individualAddress>}

    @ivar _inQueue: input queue
    @type _inQueue: L{PriorityQueue}

    @ivar _outQueue: output queue
    @type _outQueue: L{PriorityQueue}

    @ivar _ldl: link data listener
    @type _ldl: L{L_DataListener<pknyx.core.layer2.l_dataListener>}

    """

    _ldl = None

    def setListener(self, ldl):
        """

        @param ldl: listener to use to receive data
        @type ldl: L{L_GroupDataListener<pknyx.core.layer2.l_groupDataListener>}
        """
        self._ldl = ldl

    def dataReq(self, cEMI):
        """
        Transmit a frame, i.e. forward to ETS.
        """
        logger.debug("L_DataService.dataReq(): cEMI=%s" % cEMI)

        # Add source address to cEMI
        if self.physAddr is NOT_REQUIRED:
            cEMI.sourceAddress = self.emi.addr
        else:
            cEMI.sourceAddress = self.physAddr

        # Let EMI distribute the packet
        super(L_DataService, self).dataReq(cEMI)

    def dataInd(self, cEMI):
        """
        Receive a frame from ETS.

        Common code for individually- and group-addressed frames.
        Distinguishing between individual and group receivers is done at
        higher levels.
        """
        srcAddr = cEMI.sourceAddress
        if self.physAddr != NOT_REQUIRED and srcAddr != self.physAddr:  # Avoid loop
            if cEMI.messageCode == CEMILData.MC_LDATA_IND:  #in (CEMILData.MC_LDATA_CON, CEMILData.MC_LDATA_IND):
                if self._ldl is None:
                    logger.warning("L_GroupDataService.run(): not listener defined")
                else:
                    self._ldl.dataInd(cEMI)
                    return True
        return False

