# -*- coding: utf-8 -*-

from pknyx.stack.flags import *
import unittest

# Mute logger
from pknyx.services.logger import logging
logger = logging.getLogger(__name__)
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
