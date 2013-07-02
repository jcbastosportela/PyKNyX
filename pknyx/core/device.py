# -*- coding: utf-8 -*-

""" Python KNX framework

License
=======

 - B{pKNyX} (U{http://www.pknyx.org}) is Copyright:
  - (C) 2013 Frédéric Mantegazza

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

Device management

Implements
==========

 - B{Device}

Documentation
=============

B{Device} is one of the most important object of B{pKNyX} framework, after L{Datapoint<pknyx.core.datapoint>}.
A device exposes one or more Datapoints, to form a high level entity. It can represents a real device (and act as
a KNX gateway for that device), or can be a virtual device, to

Usage
=====

@author: Frédéric Mantegazza
@copyright: (C) 2013 Frédéric Mantegazza
@license: GPL
"""

__revision__ = "$Id$"

from pknyx.common.exception import PKNyXValueError
from pknyx.logging.loggingServices import Logger
from pknyx.core.datapoint import Datapoint
from pknyx.stack.individualAddress import IndividualAddress


class DeviceValueError(PKNyXValueError):
    """
    """


class Device(object):
    """ Device class

    The Datapoint of a Device must be defined in sub-classes, as class dict, and named B{DP_xxx}. They will be
    automatically instanciated as real L{Datapoint} objects, and added to the B{_dp} dict.

    @ivar _name: name of the device
    @type _name:str

    @ivar _desc: description of the device
    @type _desc:str

    @ivar _address: source address used when transmitting on the bus
    @type _address: L{IndividualAddress}

    @ivar _dp: Datapoint exposed by this Datapoint
    @type _dp: dict of L{Datapoint}
    """
    def __new__(cls, *args, **kwargs):
        """ Init the class with all available types for this DPT

        All class objects defined in sub-classes name B{DP_xxx}, will be treated as Datapoint (aka Group Objects) and
        added to the B{_dp} dict.
        """
        self = object.__new__(cls, *args, **kwargs)
        self._dp = {}
        self._desc = None
        for key, value in cls.__dict__.iteritems():
            if key.startswith("DP_"):
                name = value['name']
                if self._dp.has_key(key):
                    raise DeviceValueError("duplicated Datapoint (%s)" % repr(key))
                self._dp[name] = Datapoint(self, **value)
            elif key == "DESC":
                self._desc = value

        return self

    def __init__(self, name, desc=None, address=IndividualAddress()):
        """

        @param name: name of the device
        @type name: str

        @param desc: description of the device
        @type desc: str

        @param address: source address used when transmitting on the bus
        @type address: L{IndividualAddress}

        raise DeviceValueError:
        """
        super(Device, self).__init__()

        self._name = name

        if desc is not None:
            self._desc = "%s - %s" % (desc, self._desc)

        if not isinstance(address, IndividualAddress):
            address = IndividualAddress(address)
        self._address = address

    def __repr__(self):
        return "<Device(name='%s', desc='%s', address='%s')>" % (self._name, self._desc, self._address)

    def __str__(self):
        return "<Device('%s')>" % self._name

    @property
    def name(self):
        return self._name

    @property
    def desc(self):
        return self._desc

    @property
    def address(self):
        return self._address

    @property
    def dp(self):
        return self._dp


if __name__ == '__main__':
    import unittest

    # Mute logger
    Logger().setLevel('error')


    class DeviceTestCase(unittest.TestCase):

        class TestDevice(Device):
            DP_01 = dict(name="temperature", dptId="9.001", flags="CRT", priority="low", defaultValue=0.)
            DP_02 = dict(name="humidity", dptId="9.007", flags="CRT", priority="low", defaultValue=0.)
            DP_03 = dict(name="wind_speed", dptId="9.005", flags="CRT", priority="low", defaultValue=0.)
            DP_04 = dict(name="wind_alarm", dptId="1.005", flags="CRT", priority="urgent", defaultValue="No alarm")
            DP_05 = dict(name="wind_speed_limit", dptId="9.005", flags="CWTU", priority="low", defaultValue=15.)
            DP_06 = dict(name="wind_alarm_enable", dptId="1.003", flags="CWTU", priority="low", defaultValue="Disable")

            DESC = "Dummy description"

        def setUp(self):
            self.dev1 = DeviceTestCase.TestDevice("test1")
            self.dev2 = DeviceTestCase.TestDevice("test2", desc="pipo")

        def tearDown(self):
            pass

        def test_display(self):
            print repr(self.dev1)
            print self.dev2

        def test_constructor(self):
            pass


    unittest.main()
