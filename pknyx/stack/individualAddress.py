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

Indivudual Address management

Implements
==========

 - B{IndividualAddressValueError}
 - B{IndividualAddress}

Documentation
=============


Usage
=====

>>> from individualAddress import IndividualAddress
>>> indAddr = IndividualAddress(1)
IndividualAddressValueError: invalid individual address
>>> indAddr = IndividualAddress("16.16.256")
IndividualAddressValueError: individual address out of range
>>> indAddr = IndividualAddress("1.2.3")
>>> indAddr
<IndividualAddress("1.2.3")>
>>> indAddr.raw
4611
>>> indAddr.address
'1.2.3'
>>> indAddr.area
1
>>> indAddr.line
2
>>> indAddr.device
3
>>> indAddr.frame
'\x12\x03'

@author: Frédéric Mantegazza
@copyright: (C) 2013-2015 Frédéric Mantegazza
@license: GPL
"""


from pknyx.common.exception import PKNyXValueError
from pknyx.services.logger import logging; logger = logging.getLogger(__name__)
from pknyx.stack.knxAddress import KnxAddress, KnxAddressValueError


class IndividualAddressValueError(KnxAddressValueError):
    """
    """


class IndividualAddress(KnxAddress):
    """ Individual address hanlding class
    """
    def __init__(self, address="0.0.0"):
        """ Create an individual address

        @param address: individual address
        @type address: str or tuple of int

        raise IndividualAddressValueError: invalid address

        @todo: add constructor with simple int
        """
        #logger.debug("IndividualAddress.__init__(): address=%s" % repr(address))

        if isinstance(address, str):
            address = address.strip().split('.')
            try:
                address = [int(val) for val in address]
            except ValueError:
                logger.exception("IndividualAddress.__init__()")
                raise IndividualAddressValueError("invalid individual address")
        try:
            if len(address) == 3:
                if not 0 <= address[0] <= 0xf or not 0 <= address[1] <= 0xf or not 0 <= address[2] <= 0xff:
                    raise IndividualAddressValueError("individual address out of range")
                address = address[0] << 12 | address[1] << 8 | address[2]
            else:
                raise IndividualAddressValueError("invalid individual address")
        except TypeError:
            if not isinstance(address, int):
                logger.exception("IndividualAddress.__init__()")
                raise IndividualAddressValueError("invalid individual address")

        super(IndividualAddress, self).__init__(address)

    def __repr__(self):
        return "<IndividualAddress('%s')>" % self.address

    def __str__(self):
        return self.address

    @property
    def address(self):
        address = []
        address.append("%d" % self.area)
        address.append("%d" % self.line)
        address.append("%d" % self.device)

        return '.'.join(address)

    @property
    def area(self):
        return self._raw >> 12 & 0xf

    @property
    def line(self):
        return self._raw >> 8 & 0xf

    @property
    def device(self):
        return self._raw & 0x0ff

