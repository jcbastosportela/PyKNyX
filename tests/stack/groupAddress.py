# -*- coding: utf-8 -*-

from pyknyx.stack.groupAddress import *
import unittest

# Mute logger
from pyknyx.services.logger import logging
logger = logging.getLogger(__name__)
logging.getLogger("pyknyx").setLevel(logging.ERROR)


class GroupAddressTestCase(unittest.TestCase):

    def setUp(self):
        self.ad1 = GroupAddress("1/2/3")
        #print self.ad1
        self.ad2 = GroupAddress("1/2")
        self.ad3 = GroupAddress((1, 2, 3))
        self.ad4 = GroupAddress((1, 2))
        self.ad5 = GroupAddress(4321)

    def tearDown(self):
        pass

    def test_display(self):
        assert repr(self.ad1) == "<GroupAddress('1/2/3')>"
        assert str(self.ad3) == '1/2/3'

    def test_constructor(self):
        #with self.assertRaises(GroupAddressValueError):
            #GroupAddress(0)
        with self.assertRaises(GroupAddressValueError):
            GroupAddress("0")
        with self.assertRaises(GroupAddressValueError):
            GroupAddress((0, 0, 0, 0))
        with self.assertRaises(GroupAddressValueError):
            GroupAddress("0/0/0/0")

        with self.assertRaises(GroupAddressValueError):
            GroupAddress((-1, 0, 0))
        with self.assertRaises(GroupAddressValueError):
            GroupAddress("-1/0/0")
        with self.assertRaises(GroupAddressValueError):
            GroupAddress((0, -1, 0))
        with self.assertRaises(GroupAddressValueError):
            GroupAddress("0/-1/0")
        with self.assertRaises(GroupAddressValueError):
            GroupAddress((0, 0, -1))
        with self.assertRaises(GroupAddressValueError):
            GroupAddress("0/0/-1")
        with self.assertRaises(GroupAddressValueError):
            GroupAddress((32, 0, 0))
        with self.assertRaises(GroupAddressValueError):
            GroupAddress("32/0/0")
        with self.assertRaises(GroupAddressValueError):
            GroupAddress((0, 8, 0))
        with self.assertRaises(GroupAddressValueError):
            GroupAddress("0/8/0")
        with self.assertRaises(GroupAddressValueError):
            GroupAddress((0, 0, 256))
        with self.assertRaises(GroupAddressValueError):
            GroupAddress("0/0/256")

        with self.assertRaises(GroupAddressValueError):
            GroupAddress((-1, 0))
        with self.assertRaises(GroupAddressValueError):
            GroupAddress("-1/0")
        with self.assertRaises(GroupAddressValueError):
            GroupAddress((0, -1))
        with self.assertRaises(GroupAddressValueError):
            GroupAddress("0/-1")
        with self.assertRaises(GroupAddressValueError):
            GroupAddress((32, 0))
        with self.assertRaises(GroupAddressValueError):
            GroupAddress("32/0")
        with self.assertRaises(GroupAddressValueError):
            GroupAddress((0, 2048))
        with self.assertRaises(GroupAddressValueError):
            GroupAddress("0/2048")

    def test_cmp(self):
        self.assertNotEqual(self.ad1, self.ad2)
        self.assertEqual(self.ad1, self.ad3)

    def test_address3(self):
        self.assertEqual(self.ad1.address, "1/2/3")
        self.assertEqual(self.ad2.address, "1/0/2")
        self.assertEqual(self.ad3.address, "1/2/3")
        self.assertEqual(self.ad4.address, "1/0/2")

    def test_address2(self):
        self.ad1.outFormatLevel = 2
        self.ad2.outFormatLevel = 2
        self.ad3.outFormatLevel = 2
        self.ad4.outFormatLevel = 2
        self.assertEqual(self.ad1.address, "1/515")
        self.assertEqual(self.ad2.address, "1/2")
        self.assertEqual(self.ad3.address, "1/515")
        self.assertEqual(self.ad4.address, "1/2")

    def test_main(self):
        self.assertEqual(self.ad1.main, 1)
        self.assertEqual(self.ad2.main, 1)
        self.assertEqual(self.ad3.main, 1)
        self.assertEqual(self.ad4.main, 1)

    def test_middle3(self):
        self.assertEqual(self.ad1.middle, 2)
        self.assertEqual(self.ad2.middle, 0)
        self.assertEqual(self.ad3.middle, 2)
        self.assertEqual(self.ad4.middle, 0)

    def test_middle2(self):
        self.ad1.outFormatLevel = 2
        self.ad2.outFormatLevel = 2
        self.ad3.outFormatLevel = 2
        self.ad4.outFormatLevel = 2
        self.assertEqual(self.ad1.middle, 0)
        self.assertEqual(self.ad2.middle, 0)
        self.assertEqual(self.ad3.middle, 0)
        self.assertEqual(self.ad4.middle, 0)

    def test_sub3(self):
        self.assertEqual(self.ad1.sub, 3)
        self.assertEqual(self.ad2.sub, 2)
        self.assertEqual(self.ad3.sub, 3)
        self.assertEqual(self.ad4.sub, 2)

    def test_sub2(self):
        self.ad1.outFormatLevel = 2
        self.ad2.outFormatLevel = 2
        self.ad3.outFormatLevel = 2
        self.ad4.outFormatLevel = 2
        self.assertEqual(self.ad1.sub, 515)
        self.assertEqual(self.ad2.sub, 2)
        self.assertEqual(self.ad3.sub, 515)
        self.assertEqual(self.ad4.sub, 2)

    def test_outFormatLevel(self):
        self.assertEqual(self.ad1.outFormatLevel, 3)
        with self.assertRaises(GroupAddressValueError):
            self.ad1.outFormatLevel = 1
        with self.assertRaises(GroupAddressValueError):
            self.ad1.outFormatLevel = 4

