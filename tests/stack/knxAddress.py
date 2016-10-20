# -*- coding: utf-8 -*-

from pknyx.stack.knxAddress import *
import unittest

# Mute logger
from pknyx.services.logger import logging
logger = logging.getLogger(__name__)
logger.root.setLevel(logging.ERROR)


class KnxAddressTestCase(unittest.TestCase):

    def setUp(self):
        self.ad1 = KnxAddress(123)
        self.ad2 = KnxAddress(b"\x22\x31")
        self.ad3 = KnxAddress(123)

    def tearDown(self):
        pass

    def test_display(self):
        print(repr(self.ad1))
        print(self.ad2)

    def test_constructor(self):
        with self.assertRaises(KnxAddressValueError):
            KnxAddress(-1)
        with self.assertRaises(KnxAddressValueError):
            KnxAddress(0x10000)
        with self.assertRaises(KnxAddressValueError):
            KnxAddress(b"\x00\x00\x00")

    def test_add(self):
        self.assertEqual((self.ad2+2).raw, 8755)

    def test_raw(self):
        self.assertEqual(self.ad2.raw, 8753)

    def test_lowhigh(self):
        self.assertEqual(self.ad2.low, 0x31)
        self.assertEqual(self.ad2.high, 0x22)

    def test_cmp(self):
        self.assertNotEqual(self.ad1, self.ad2)
        self.assertEqual(self.ad1, self.ad3)

    def test_frame(self):
        self.assertEqual(self.ad1.frame, b"\x00\x7b")

