# -*- coding: utf-8 -*-

from pknyx.core.dptXlator.dptXlator4ByteFloat import *
import unittest

# Mute logger
from pknyx.services.logger import logging
logger = logging.getLogger(__name__)
logging.getLogger("pknyx").setLevel(logging.ERROR)

class DPT4ByteFloatTestCase(unittest.TestCase):

    def setUp(self):
        self.testTable = (
            (-340282346638528859811704183484516925440, 0xff7fffff, b"\xff\x7f\xff\xff"),
            (                                      -1, 0xbf800000, b"\xbf\x80\x00\x00"),
            (                                       0, 0x00000000, b"\x00\x00\x00\x00"),
            (                                       1, 0x3f800000, b"\x3f\x80\x00\x00"),
            ( 340282346638528859811704183484516925440, 0x7f7fffff, b"\x7f\x7f\xff\xff"),
        )
        self.dptXlator = DPTXlator4ByteFloat("14.xxx")

    def tearDown(self):
        pass

    #def test_constructor(self):
        #print self.dptXlator.handledDPT

    def test_typeSize(self):
        self.assertEqual(self.dptXlator.typeSize, 4)

    def testcheckValue(self):
        with self.assertRaises(DPTXlatorValueError):
            self.dptXlator.checkValue(self.dptXlator._dpt.limits[1] * 10)

    def test_dataToValue(self):
        for value, data, frame in self.testTable:
            value_ = self.dptXlator.dataToValue(data)
            self.assertEqual(value_, value, "Conversion failed (converted value for %s is %.f, should be %.f)" %
                                (hex(data), value_, value))

    def test_valueToData(self):
        for value, data, frame in self.testTable:
            data_ = self.dptXlator.valueToData(value)
            self.assertEqual(data_, data, "Conversion failed (converted data for %.f is %s, should be %s)" %
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
