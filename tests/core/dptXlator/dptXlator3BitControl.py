# -*- coding: utf-8 -*-

from pyknyx.core.dptXlator.dptXlator3BitControl import *
import unittest

# Mute logger
from pyknyx.services.logger import logging
logger = logging.getLogger(__name__)
logging.getLogger("pyknyx").setLevel(logging.ERROR)

class DPT3BitControlTestCase(unittest.TestCase):

    def setUp(self):
        self.testTable = (
            ( 0, 0x00, b'\x00'),
            ( 1, 0x09, b'\x09'),
            (-1, 0x01, b'\x01'),
            ( 7, 0x0f, b'\x0f'),
            (-7, 0x07, b'\x07'),
        )
        self.stepCodeIntervalTable = (
            (1,  1),
            (2,  2),
            (3,  4),
            (4,  8),
            (5, 16),
            (6, 32),
            (7, 64),
        )
        self.dptXlator = DPTXlator3BitControl("3.xxx")

    def tearDown(self):
        pass

    #def test_constructor(self):
        #print self.dptXlator.handledDPT

    def test_typeSize(self):
        self.assertEqual(self.dptXlator.typeSize, 0)

    def testcheckValue(self):
        with self.assertRaises(DPTXlatorValueError):
            self.dptXlator.checkValue(self.dptXlator.dpt.limits[1] + 1)

    def test_dataToValue(self):
        for value, data, frame in self.testTable:
            value_ = self.dptXlator.dataToValue(data)
            self.assertEqual(value_, value, "Conversion failed (converted value for %s is %d, should be %d)" %
                                (hex(data), value_, value))

    def test_valueToData(self):
        for value, data, frame in self.testTable:
            data_ = self.dptXlator.valueToData(value)
            self.assertEqual(data_, data, "Conversion failed (converted data for %d is %s, should be %s)" %
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

    #def test_nbIntervalsToStepCode(self):
        #for stepCode, nbIntervals in self.stepCodeIntervalTable:
            #nbIntervals_ = self.dptXlator.stepCodeToNbIntervals(stepCode)
            #self.assertEqual(nbIntervals_, nbIntervals, "Conversion failed (computed nbIntervals for stepCode %d is %d, should be %d)" %
                                #(stepCode, nbIntervals_, nbIntervals))

    #def test_stepCodeToNbIntervals(self):
        #for stepCode, nbIntervals in self.stepCodeIntervalTable:
            #stepCode_ = self.dptXlator.nbIntervalsToStepCode(nbIntervals)
            #self.assertEqual(stepCode_, stepCode, "Conversion failed (computed stepCode for %d intervals is %d, should be %d)" %
                                #(nbIntervals, stepCode_, stepCode))

