# -*- coding: utf-8 -*-

from pknyx.core.dptXlator.dptXlatorScene import *
import unittest

# Mute logger
from pknyx.services.logger import logging
logger = logging.getLogger(__name__)
logger.root.setLevel(logging.ERROR)

class DPTSceneTestCase(unittest.TestCase):

    def setUp(self):
        self.testTable = (
            ((0,  0), 0x00, b"\x00"),
            ((0,  1), 0x01, b"\x01"),
            ((0, 63), 0x3f, b"\x3f"),
            ((1,  0), 0x80, b"\x80"),
            ((1,  1), 0x81, b"\x81"),
            ((1, 63), 0xbf, b"\xbf"),
        )
        self.dptXlator = DPTXlatorScene("17.001")

    def tearDown(self):
        pass

    #def test_constructor(self):
        #print self.dptXlator.handledDPT

    def test_typeSize(self):
        self.assertEqual(self.dptXlator.typeSize, 1)

    def testcheckValue(self):
        with self.assertRaises(DPTXlatorValueError):
            self.dptXlator.checkValue((-1, 0))
        with self.assertRaises(DPTXlatorValueError):
            self.dptXlator.checkValue((0, -1))

        with self.assertRaises(DPTXlatorValueError):
            self.dptXlator.checkValue((0, 64))
        with self.assertRaises(DPTXlatorValueError):
            self.dptXlator.checkValue((2, 0))

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
