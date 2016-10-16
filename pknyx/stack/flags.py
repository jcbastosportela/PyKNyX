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

Flags management

Implements
==========

 - B{FlagsValueError}
 - B{Flags}

Documentation
=============

L{Flags} class handles L{GroupObject<pknyx.core.groupObject>} bus behaviour.

Meaning of each flag for the GroupObject, when set:
 - C - comm.:     may transmit to the KNX bus
 - R - read:      send a response with its Datapoint value to the bus when it receives a Read request
 - W - write:     update its Datapoint value when it receives a Write request
 - T - transmit:  send its Datapoint value to the first bounded GAD when it changes
 - U - update:    update its Datapoint value if it receives a Response request
 - I - init:      sends a Read request at startup
 - S - stateless: like T, but transmits its Datapoint value even if it didn't change (useful for scenes)

Note: only one Datapoint per GAD should have its R flag set.

Flags in ETS:
 - en: S   C   R   W   T   U
 - fr: S   K   L   E   T   Act

Usage
=====

An actor will have a single data point with one group object CW (receiving
a command for setting the output) and another group object CRT (the
output's state).

An input will have one data point with a group object CT (send a command)
and another data point with its group object CWUI (receive the actor's state).
A "toggle" command reads the second DP's state, inverts it, and writes it
to the first DP.

The master-off switch will have one data point CS.

A shadow actor, i.e. an actor that monitors another actor's state, will
have one data point CWUI (receive state). It may have another (W) that
monitors the actual command. Such an actor is able to issue an alert if
there is no state-has-changed Write after a (command, state-changing)
Write.

@author: Frédéric Mantegazza
@copyright: (C) 2013-2015 Frédéric Mantegazza
@license: GPL
"""


import re

from pknyx.common.exception import PKNyXValueError
from pknyx.services.logger import logging; logger = logging.getLogger(__name__)


class FlagsValueError(PKNyXValueError):
    """
    """


class Flags(object):
    """ Flag class

    @ivar _raw: raw set of flags
    @type _raw: str
    """
    def __init__(self, raw="CRT"):
        """ Create a new set of flags

        @param raw: raw set of flags
        @type raw: str

        raise FlagsValueError: invalid flags

        @todo: allow +xx and -xx usage
        """
        super(Flags, self).__init__()

        try:
            if not re.match("^C?R?W?T?U?I?S?$", raw):
                raise FlagsValueError("invalid flags set (%r)" % repr(raw))
        except:
            logger.exception("Flags.__init__()")
            raise FlagsValueError("invalid flags set (%r)" % repr(raw))
        self._raw = raw

    def __repr__(self):
        return "<Flags('%s')>" % self._raw

    def __str__(self):
        return self._raw

    def __call__(self, value):
        return self.test(value)

    def test(self, value):
        """ Test if value matching flag is set

        @param value: flag(s) to test
        @type value: str

        @return: True if all value macthing flags are set
        @rtype: bool
        """
        for flag in value:
            if flag not in self._raw:
                return False

        return True

    @property
    def raw(self):
        return self._raw

    @property
    def communicate(self):
        return 'C' in self._raw

    @property
    def read(self):
        return 'R' in self._raw

    @property
    def write(self):
        return 'W' in self._raw

    @property
    def transmit(self):
        return 'T' in self._raw

    @property
    def update(self):
        return 'U' in self._raw

    @property
    def init(self):
        return 'I' in self._raw

    @property
    def stateless(self):
        return 'S' in self._raw


if __name__ == '__main__':
    import unittest

    # Mute logger
    logger.root.setLevel(logging.ERROR)


    class DFlagsTestCase(unittest.TestCase):

        def setUp(self):
            self.flags = Flags("CRWTUIS")

        def tearDown(self):
            pass

        def test_display(self):
            print(repr(self.flags))
            print(self.flags)

        def test_constructor(self):
            with self.assertRaises(FlagsValueError):
                Flags("A")
            with self.assertRaises(FlagsValueError):
                Flags("CWUT")
            with self.assertRaises(FlagsValueError):
                Flags("CCWUT")
            with self.assertRaises(FlagsValueError):
                Flags("CRWTUISA")

        def test_properties(self):
            self.assertEqual(self.flags.raw, "CRWTUIS")
            self.assertEqual(self.flags.communicate, True)
            self.assertEqual(self.flags.read, True)
            self.assertEqual(self.flags.write, True)
            self.assertEqual(self.flags.transmit, True)
            self.assertEqual(self.flags.update, True)
            self.assertEqual(self.flags.init, True)
            self.assertEqual(self.flags.stateless, True)

        def test_callable(self):
            self.assertFalse(self.flags("A"))
            self.assertFalse(self.flags("ABD"))
            self.assertTrue(self.flags("C"))
            self.assertTrue(self.flags("W"))
            self.assertTrue(self.flags("CRT"))
            self.assertTrue(self.flags("CRTWIUS"))

    unittest.main()
