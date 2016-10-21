# -*- coding: utf-8 -*-

from pknyx.core.dptXlator.dptXlatorTime import *
import unittest

# Mute logger
from pknyx.services.logger import logging
logger = logging.getLogger(__name__)
logging.getLogger("pknyx").setLevel(logging.ERROR)

class DPTTimeTestCase(unittest.TestCase):

    def setUp(self):
        self.testTable = (
            ((0,  0,  0,  0), 0x000000, b"\x00\x00\x00"),
            ((1,  2,  3,  4), 0x220304, b"\x22\x03\x04"),
            ((7, 23, 59, 59), 0xf73b3b, b"\xf7\x3b\x3b"),
        )
        self.dptXlator = DPTXlatorTime("10.001")

    def tearDown(self):
        pass

    #def test_constructor(self):
        #print self.dptXlator.handledDPT

    def test_typeSize(self):
        self.assertEqual(self.dptXlator.typeSize, 3)

    def testcheckValue(self):
        with self.assertRaises(DPTXlatorValueError):
            self.dptXlator.checkValue((-1, 0, 0, 0))
        with self.assertRaises(DPTXlatorValueError):
            self.dptXlator.checkValue((0, -1, 0, 0))
        with self.assertRaises(DPTXlatorValueError):
            self.dptXlator.checkValue((0, 0, -1, 0))
        with self.assertRaises(DPTXlatorValueError):
            self.dptXlator.checkValue((0, 0, 0, -1))

        with self.assertRaises(DPTXlatorValueError):
            self.dptXlator.checkValue((8, 23, 59, 59))
        with self.assertRaises(DPTXlatorValueError):
            self.dptXlator.checkValue((7, 24, 59, 59))
        with self.assertRaises(DPTXlatorValueError):
            self.dptXlator.checkValue((7, 23, 60, 59))
        with self.assertRaises(DPTXlatorValueError):
            self.dptXlator.checkValue((7, 23, 59, 60))

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
