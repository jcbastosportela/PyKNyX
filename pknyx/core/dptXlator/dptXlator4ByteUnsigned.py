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

Datapoint Types management

Implements
==========

 - B{DPTXlator4ByteUnsigned}

Usage
=====

see L{DPTXlatorBoolean}

@author: Frédéric Mantegazza
@author: B. Malinowsky
@copyright: (C) 2013-2015 Frédéric Mantegazza
@copyright: (C) 2006, 2011 B. Malinowsky
@license: GPL
"""

import struct

from pknyx.services.logger import logging; logger = logging.getLogger(__name__)
from pknyx.core.dptXlator.dptId import DPTID
from pknyx.core.dptXlator.dpt import DPT
from pknyx.core.dptXlator.dptXlatorBase import DPTXlatorBase, DPTXlatorValueError


class DPTXlator4ByteUnsigned(DPTXlatorBase):
    """ DPTXlator class for 4-Byte-Unsigned (U32) KNX Datapoint Type

     - 4 Byte Unsigned: UUUUUUUU UUUUUUUU UUUUUUUU UUUUUUUU
     - U: Bytes [0:4294967295]

    .
    """
    DPT_Generic = DPT("12.xxx", "Generic", (0, 4294967295))

    DPT_Value_4_Ucount = DPT("12.001", "Unsigned count", (0, 4294967295), "pulses")

    def __init__(self, dptId):
        super(DPTXlator4ByteUnsigned, self).__init__(dptId, 4)

    def checkData(self, data):
        if not 0x00000000 <= data <= 0xffffffff:
            raise DPTXlatorValueError("data %s not in (0x00000000, 0xffffffff)" % hex(data))

    def checkValue(self, value):
        if not self._dpt.limits[0] <= value <= self._dpt.limits[1]:
            raise DPTXlatorValueError("Value not in range %r" % repr(self._dpt.limits))

    def dataToValue(self, data):
        value = data
        #logger.debug("DPTXlator4ByteUnsigned._toValue(): value=%d" % value)
        return value

    def valueToData(self, value):
        data = value
        #logger.debug("DPTXlator4ByteUnsigned.valueToData(): data=%s" % hex(data))
        return data

    def dataToFrame(self, data):
        return bytearray(struct.pack(">L", data))

    def frameToData(self, frame):
        data = struct.unpack(">L", frame)[0]
        return data

