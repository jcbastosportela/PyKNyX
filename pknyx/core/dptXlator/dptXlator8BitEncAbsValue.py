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

Datapoint Types management.

Implements
==========

 - B{DPTXlator8BitEncAbsValue}

Usage
=====

see L{DPTXlatorBoolean}

@author: Frédéric Mantegazza
@author: B. Malinowsky
@copyright: (C) 2013-2015 Frédéric Mantegazza
@copyright: (C) 2006, 2012 B. Malinowsky
@license: GPL
"""

import struct

from pknyx.services.logger import logging; logger = logging.getLogger(__name__)
from pknyx.core.dptXlator.dptId import DPTID
from pknyx.core.dptXlator.dpt import DPT
from pknyx.core.dptXlator.dptXlatorBase import DPTXlatorBase, DPTXlatorValueError


class DPTXlator8BitEncAbsValue(DPTXlatorBase):
    """ DPTXlator class for 8-Bit-Absolute-Encoding-Value (N8) KNX Datapoint Type

     - 1 Byte: NNNNNNNN
     - N: Byte [0:255]

    .
    """
    DPT_Generic = DPT("20.xxx", "Generic", (0, 255))

    DPT_OccMode = DPT("20.003", "Occupancy mode", ("occupied", "standby", "not occupied"))

    def __init__(self, dptId):
        super(DPTXlator8BitEncAbsValue, self).__init__(dptId, 1)

    def checkData(self, data):
        if not 0x00 <= data <= 0xff:
            raise DPTXlatorValueError("data %s not in (0x00, 0xff)" % hex(data))

    def checkValue(self, value):
        if self.dpt is self.DPT_Generic:
            if not self._dpt.limits[0] <= value <= self._dpt.limits[1]:
                raise DPTXlatorValueError("value not in range %r" % repr(self._dpt.limits))
        elif value not in self._dpt.limits:
            raise DPTXlatorValueError("value not in %r" % repr(self._dpt.limits))

    def dataToValue(self, data):
        if self.dpt is self.DPT_Generic:
            value = data
        else:
            value = self._dpt.limits[data]
        #logger.debug("DPTXlator8BitEncAbsValue.dataToValue(): value=%d" % value)
        return value

    def valueToData(self, value):
        #logger.debug("DPTXlator8BitEncAbsValue.valueToData(): value=%d" % value)
        self.checkValue(value)
        if self.dpt is self.DPT_Generic:
            data = value
        else:
            data = self._dpt.limits.index(value)
        #logger.debug("DPTXlator8BitEncAbsValue.valueToData(): data=%s" % hex(data))
        return data

    def dataToFrame(self, data):
        return bytearray(struct.pack(">B", data))

    def frameToData(self, frame):
        data = struct.unpack(">B", frame)[0]
        return data

