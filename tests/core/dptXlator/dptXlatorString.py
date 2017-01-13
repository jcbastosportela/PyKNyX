# -*- coding: utf-8 -*-

from pyknyx.core.dptXlator.dptXlatorString import *
import unittest

# Mute logger
from pyknyx.services.logger import logging
logger = logging.getLogger(__name__)
logging.getLogger("pyknyx").setLevel(logging.ERROR)

class DPTStringTestCase(unittest.TestCase):

    def setUp(self):
        self.testTable = (
            (14 * (0,),                                            0x0000000000000000000000000000, 14 * b"\x00"),
            ((48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 0, 0, 0, 0), 0x3031323334353637383900000000, b"0123456789\x00\x00\x00\x00"),
            (14 * (255,),                                          0xffffffffffffffffffffffffffff, 14 * b"\xff"),
        )
        self.dptXlator = DPTXlatorString("16.001")

    def tearDown(self):
        pass

    #def test_constructor(self):
        #print self.dptXlator.handledDPT

    def test_typeSize(self):
        self.assertEqual(self.dptXlator.typeSize, 14)

    #def testcheckValue(self):
        #with self.assertRaises(DPTXlatorValueError):
            #self.dptXlator.checkValue((0, 1, 1969))

    def test_dataToValue(self):
        for value, data, frame in self.testTable:
            value_ = self.dptXlator.dataToValue(data)
            self.assertEqual(value_, value, "Conversion failed (converted value for %s is %s, should be %s)" %
                                (hex(data), value_, value))

    def test_valueToData(self):
        for value, data, frame in self.testTable:
            data_ = self.dptXlator.valueToData(value)
            self.assertEqual(data_, data, "Conversion failed (converted data for %s is %s, should be %s)" %
                                (value, hex(data_), hex(data)))

    def test_dataToFrame(self):
        for value, data, frame in self.testTable:
            frame_ = self.dptXlator.dataToFrame(data)
            self.assertEqual(frame_, frame, "Conversion failed (converted frame for %s is %r, should be %r)" %
                                (hex(data), frame_, frame))

    def test_frameToData(self):
        for value, data, frame in self.testTable:
            data_ = self.dptXlator.frameToData(frame)
            self.assertEqual(data_, data, "Conversion failed (converted data for %r is %s, should be %s)" %
                                (frame, hex(data_), hex(data)))
