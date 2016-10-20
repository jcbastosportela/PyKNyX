# -*- coding: utf-8 -*-

from pknyx.stack.cemi.cemiLData import *
import unittest

# Mute logger
logger.root.setLevel(logging.ERROR)


class CEMILDataTestCase(unittest.TestCase):

    def setUp(self):
        self.frame1 = CEMILData()
        self.frame2 = CEMILData(")\x00\xbc\xd0\x11\x0e\x19\x02\x01\x00\x80")
        self.frame3 = CEMILData(")\x00\xbc\xd0\x11\x04\x10\x04\x03\x00\x80\x19,")

    def tearDown(self):
        pass

    def test_display(self):
        print(repr(self.frame2))
        print(self.frame3)

    def test_constructor(self):
        with self.assertRaises(CEMIValueError):
            CEMILData(")\x03\xff\xff\xff\xbc\xd0\x11\x04\x10\x04\x03\x00\x80\x19,")  # ext frame

