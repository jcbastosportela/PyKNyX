# -*- coding: utf-8 -*-

from pknyx.core.dptXlator.dptXlatorDate import *
import unittest

# Mute logger
logger.root.setLevel(logging.ERROR)

class DPTDateTestCase(unittest.TestCase):

    def setUp(self):
        self.testTable = (
            (( 1,  1, 2000), 0x010100, "\x01\x01\x00"),
            (( 1,  1, 2068), 0x010144, "\x01\x01\x44"),
            (( 1,  1, 1969), 0x010145, "\x01\x01\x45"),
            ((31, 12, 1999), 0x1f0c63, "\x1f\x0c\x63"),
        )
        self.dptXlator = DPTXlatorDate("11.001")

    def tearDown(self):
        pass

    #def test_constructor(self):
        #print self.dptXlator.handledDPT

    def test_typeSize(self):
        self.assertEqual(self.dptXlator.typeSize, 3)

    def testcheckValue(self):
        with self.assertRaises(DPTXlatorValueError):
            self.dptXlator.checkValue((0, 1, 1969))
        with self.assertRaises(DPTXlatorValueError):
            self.dptXlator.checkValue((1, 0, 1969))
        with self.assertRaises(DPTXlatorValueError):
            self.dptXlator.checkValue((1, 1, 1968))

        with self.assertRaises(DPTXlatorValueError):
            self.dptXlator.checkValue((32, 12, 2068))
        with self.assertRaises(DPTXlatorValueError):
            self.dptXlator.checkValue((31, 13, 2068))
        with self.assertRaises(DPTXlatorValueError):
            self.dptXlator.checkValue((31, 12, 2069))

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
