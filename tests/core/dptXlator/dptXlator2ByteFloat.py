# -*- coding: utf-8 -*-

from pknyx.core.dptXlator.dptXlator2ByteFloat import *
import unittest

# Mute logger
from pknyx.services.logger import logging
logger = logging.getLogger(__name__)
logger.root.setLevel(logging.ERROR)

class DPTXlator2ByteFloatTestCase(unittest.TestCase):

    def setUp(self):
        self.testTable = (
            (     0.,   0x0000, "\x00\x00"),
            (     0.01, 0x0001, "\x00\x01"),
            (    -0.01, 0x87ff, "\x87\xff"),
            (    -1.,   0x879c, "\x87\x9c"),
            (     1.,   0x0064, "\x00\x64"),
            (  -272.96, 0xa156, "\xa1\x56"),
            (670760.96, 0x7fff, "\x7f\xff"),
        )
        self.dptXlator = DPTXlator2ByteFloat("9.xxx")

    def tearDown(self):
        pass

    #def test_constructor(self):
        #print self.dptXlator.handledDPT

    def test_typeSize(self):
        self.assertEqual(self.dptXlator.typeSize, 2)

    def testcheckValue(self):
        with self.assertRaises(DPTXlatorValueError):
            self.dptXlator.checkValue(self.dptXlator._dpt.limits[1] + 1)

    def test_dataToValue(self):
        for value, data, frame in self.testTable:
            value_ = self.dptXlator.dataToValue(data)
            self.assertEqual(value_, value, "Conversion failed (converted value for %s is %.2f, should be %.2f)" %
                                (hex(data), value_, value))

    def test_valueToData(self):
        for value, data, frame in self.testTable:
            data_ = self.dptXlator.valueToData(value)
            self.assertEqual(data_, data, "Conversion failed (converted data for %.2f is %s, should be %s)" %
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

