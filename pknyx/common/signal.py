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

Signal/slot pattern

Implements
==========

 - B{Signal}
 - B{_WeakMethod_FuncHost}
 - B{_WeakMethod}

Documentation
=============

To use, simply create a B{Signal} instance. The instance may be a member of a class, a global, or a local; it makes no
difference what scope it resides within. Connect slots to the signal using the B{connect()} method.

The slot may be a member of a class or a simple function. If the slot is a member of a class, Signal will automatically
detect when the method's class instance has been deleted and remove it from its list of connected slots.

This class was generously donated by a poster on ASPN see U{http://aspn.activestate.com}

Usage
=====

>>> sig = Signal()
>>> def test(value): print("test(): %s" % repr(value))
>>> sig.connect(test)
>>> sig.emit("Hello World!")
test(): 'Hello World!'
>>> sig.disconnect(test)
>>> sig.emit("Hello World!")

@author: Frédéric Mantegazza
@copyright: (C) 2013-2015 Frédéric Mantegazza
@license: GPL
"""

import os
import os.path
import weakref
import inspect

#from pknyx.services.logger import logging; logger = logging.getLogger(__name__)

from blinker import Signal as BlinkerSignal

class Signal(BlinkerSignal):
    """Signal, using Blinker."""
    def __call__(self, *args, **kwargs):
        self.emit(*args, **kwargs)

    def emit(self, *args, **kwargs):
        """ Emit the signal.

        @todo: add try/except?
        """
        return self.send(*args, **kwargs)

    def disconnectAll(self):
        """ Disconnect all slots from the signal
        """
        self._clear_state()
