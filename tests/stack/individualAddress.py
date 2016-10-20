# -*- coding: utf-8 -*-

from pknyx.stack.individualAddress import *
import unittest

# Mute logger
logger.root.setLevel(logging.ERROR)


class IndividualAddressTestCase(unittest.TestCase):

    def setUp(self):
        self.ad1 = IndividualAddress("1.2.3")
        self.ad2 = IndividualAddress((1, 2, 3))
        self.ad3 = IndividualAddress((1, 2, 4))
        self.ad4 = IndividualAddress(1256)

    def tearDown(self):
        pass

    def test_display(self):
        print(repr(self.ad1))
        print(self.ad2)

    def test_constructor(self):
        #with self.assertRaises(IndividualAddressValueError):
            #IndividualAddress(0)
        with self.assertRaises(IndividualAddressValueError):
            IndividualAddress("0")
        with self.assertRaises(IndividualAddressValueError):
            IndividualAddress((0, 0))
        with self.assertRaises(IndividualAddressValueError):
            IndividualAddress("0.0")
        with self.assertRaises(IndividualAddressValueError):
            IndividualAddress((0, 0, 0, 0))
        with self.assertRaises(IndividualAddressValueError):
            IndividualAddress("0.0.0.0")

        with self.assertRaises(IndividualAddressValueError):
            IndividualAddress((-1, 0, 0))
        with self.assertRaises(IndividualAddressValueError):
            IndividualAddress("-1.0.0")
        with self.assertRaises(IndividualAddressValueError):
            IndividualAddress((0, -1, 0))
        with self.assertRaises(IndividualAddressValueError):
            IndividualAddress("0.-1.0")
        with self.assertRaises(IndividualAddressValueError):
            IndividualAddress((0, 0, -1))
        with self.assertRaises(IndividualAddressValueError):
            IndividualAddress("0.0.-1")
        with self.assertRaises(IndividualAddressValueError):
            IndividualAddress((16, 0, 0))
        with self.assertRaises(IndividualAddressValueError):
            IndividualAddress("16.0.0")
        with self.assertRaises(IndividualAddressValueError):
            IndividualAddress((0, 16, 0))
        with self.assertRaises(IndividualAddressValueError):
            IndividualAddress("0.16.0")
        with self.assertRaises(IndividualAddressValueError):
            IndividualAddress((0, 0, 256))
        with self.assertRaises(IndividualAddressValueError):
            IndividualAddress("0.0.256")

    def test_cmp(self):
        self.assertNotEqual(self.ad1, self.ad3)
        self.assertEqual(self.ad1, self.ad2)

    def test_address(self):
        self.assertEqual(self.ad1.address, "1.2.3")
        self.assertEqual(self.ad2.address, "1.2.3")

    def test_area(self):
        self.assertEqual(self.ad1.area, 1)
        self.assertEqual(self.ad2.area, 1)

    def test_line(self):
        self.assertEqual(self.ad1.line, 2)
        self.assertEqual(self.ad2.line, 2)

    def test_device(self):
        self.assertEqual(self.ad1.device, 3)
        self.assertEqual(self.ad2.device, 3)

