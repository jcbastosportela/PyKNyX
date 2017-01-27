# -*- coding: utf-8 -*-

""" Python KNX framework

License
=======

 - B{PyKNyX} (U{http://www.pyknyx.org}) is Copyright:
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

Result error codes

Implements
==========

 - B{Result}
 - B{ResultValueError}

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


class ResultValueError(PyKNyXValueError):
    """
    """


class Result(object):
    """ Result class

    Contant definitions of return codes of the transmission functions of the EIB protocol stack.
    """
    OK = 0         # Message was successfully transmitted
    ERROR = 1      # Layer 2: unspecified error
                   # (Due to standard EIB-BCU's return no specific error codes, i.e.
                   #  stands for LINE_BUSY, NO_ACK, NACK or DEST_BUSY respectively.)
    LINE_BUSY = 2  # Layer 2: message timed out cause transmission line was busy
    NO_ACK = 3     # Layer 2: message was transmitted, but no acknowledge was received
    NACK = 4       # Layer 2: message was transmitted, but L2-NACK received
    DEST_BUSY = 5  # Layer 2: message was transmitted, but destination sent BUSY

    AVAILABLE_CODES = (OK,
                       ERROR,
                       LINE_BUSY,
                       NO_ACK,
                       NACK,
                       DEST_BUSY
                      )

    def __init__(self):
        """

        raise ResultValueError:
        """
        super(Result, self).__init__()

