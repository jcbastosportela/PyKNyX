# -*- coding: utf-8 -*-

from pknyx.stack.cemi.cemiLDataFrame import *
import unittest

# Mute logger
logger.root.setLevel(logging.ERROR)


class CEMILDataFrameTestCase(unittest.TestCase):

    def setUp(self):
        self.frame1 = CEMILDataFrame()
        self.frame2 = CEMILDataFrame(")\x00\xbc\xd0\x11\x0e\x19\x02\x01\x00\x80")
        self.frame3 = CEMILDataFrame(")\x00\xbc\xd0\x11\x04\x10\x04\x03\x00\x80\x19,")
        self.frame4 = CEMILDataFrame(addIL=2)
        self.frame5 = CEMILDataFrame(")\x03\xff\xff\xff\xbc\xd0\x11\x04\x10\x04\x03\x00\x80\x19,")  # ext frame

    def tearDown(self):
        pass

    def test_display(self):
        print(repr(self.frame2))
        print(self.frame3)

    def test_constructor(self):
        with self.assertRaises(CEMIValueError):
            CEMILDataFrame(frame=bytearray(10), addIL=1)  # too much args
        with self.assertRaises(CEMIValueError):
            CEMILDataFrame(frame=bytearray(5))  # frame too short

    def test_raw(self):
        self.assertEqual(self.frame1.raw, bytearray(9))
        self.assertEqual(self.frame2.raw, ")\x00\xbc\xd0\x11\x0e\x19\x02\x01\x00\x80")

    def test_mc(self):
        self.assertEqual(self.frame1.mc, 0)
        self.frame1.mc = 1
        self.assertEqual(self.frame1.mc, 1)
        self.assertEqual(self.frame2.mc, 0x29)

    def test_addIL(self):
        self.assertEqual(self.frame1.addIL, 0)
        with self.assertRaises(AttributeError):
            self.frame1.addIL = 1
        self.assertEqual(self.frame2.addIL, 0)
        self.assertEqual(self.frame4.addIL, 2)
        self.assertEqual(self.frame5.addIL, 3)

    def test_addInfo(self):
        self.assertEqual(self.frame1.addInfo, None)
        with self.assertRaises(CEMIValueError):
            self.frame2.addInfo = '\x00'
        self.assertEqual(self.frame2.addInfo, None)
        self.assertEqual(self.frame4.addInfo, '\x00\x00')
        with self.assertRaises(CEMIValueError):
            self.frame4.addInfo = '\x00'  # not enough values
        self.frame4.addInfo = '\xff\xff'
        self.assertEqual(self.frame4.addInfo, '\xff\xff')
        self.assertEqual(self.frame5.addInfo, '\xff\xff\xff')
        self.frame5.addInfo = '\x00\x00\x00'
        self.assertEqual(self.frame5.addInfo, '\x00\x00\x00')

    def test_ctrl1(self):
        self.assertEqual(self.frame1.ctrl1, 0)
        self.frame1.ctrl1 = 0xff
        self.assertEqual(self.frame1.ctrl1, 0xff)
        self.assertEqual(self.frame2.ctrl1, 0xbc)

    def test_ctrl2(self):
        self.assertEqual(self.frame1.ctrl2, 0)
        self.frame1.ctrl2 = 0xff
        self.assertEqual(self.frame1.ctrl2, 0xff)
        self.assertEqual(self.frame2.ctrl2, 0xd0)

    def test_sah(self):
        self.assertEqual(self.frame1.sah, 0)
        self.frame1.sah = 1
        self.assertEqual(self.frame1.sah, 1)
        self.assertEqual(self.frame2.sah, 17)

    def test_sal(self):
        self.assertEqual(self.frame1.sal, 0)
        self.frame1.sal = 1
        self.assertEqual(self.frame1.sal, 1)
        self.assertEqual(self.frame2.sal, 14)

    def test_sa(self):
        self.assertEqual(self.frame1.sa, 0)
        self.frame1.sa = 1000
        self.assertEqual(self.frame1.sa, 1000)
        self.assertEqual(self.frame2.sa, 4366)

    def test_dah(self):
        self.assertEqual(self.frame1.dah, 0)
        self.frame1.dah = 1
        self.assertEqual(self.frame1.dah, 1)
        self.assertEqual(self.frame2.dah, 25)

    def test_dal(self):
        self.assertEqual(self.frame1.dal, 0)
        self.frame1.dal = 1
        self.assertEqual(self.frame1.dal, 1)
        self.assertEqual(self.frame2.dal, 2)

    def test_da(self):
        self.assertEqual(self.frame1.da, 0)
        self.frame1.sa = 2000
        self.assertEqual(self.frame1.sa, 2000)
        self.assertEqual(self.frame2.da, 6402)

    def test_npdu(self):
        self.assertEqual(self.frame1.npdu, '\x00')
        self.frame1.npdu = '\xff\xff'
        self.assertEqual(self.frame1.npdu, '\xff\xff')
        self.assertEqual(self.frame2.npdu, '\x01\x00\x80')
        self.assertEqual(self.frame3.npdu, '\x03\x00\x80\x19,')
