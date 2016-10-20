# -*- coding: utf-8 -*-

from pknyx.core.dptXlator.dptId import *
import unittest

# Mute logger
logger.root.setLevel(logging.ERROR)


class DPTIDTestCase(unittest.TestCase):

    def setUp(self):
        self.dptId = DPTID("9.003")
        self.dptId1 = DPTID("1.xxx")
        self.dptId2 = DPTID("1.001")
        self.dptId3 = DPTID("3.xxx")
        self.dptId4 = DPTID("3.001")
        self.dptId5 = DPTID("9.xxx")
        self.dptId6 = DPTID("9.001")
        self.dptId7 = DPTID("9.001")

    def tearDown(self):
        pass

    def test_display(self):
        print(repr(self.dptId))
        print(self.dptId1)

    def test_constructor(self):
        with self.assertRaises(DPTIDValueError):
            DPTID("1.00")
        with self.assertRaises(DPTIDValueError):
            DPTID(".001")
        with self.assertRaises(DPTIDValueError):
            DPTID("001.0010")
        with self.assertRaises(DPTIDValueError):
            DPTID("0001.001")

    def test_cmp(self):
        dptIds = [self.dptId3, self.dptId6, self.dptId1, self.dptId2, self.dptId5, self.dptId4, self.dptId7]
        dptIds.sort()
        sortedDptIds = [self.dptId1, self.dptId2, self.dptId3, self.dptId4, self.dptId5, self.dptId6, self.dptId7]
        self.assertEqual(dptIds, sortedDptIds)

    def test_main(self):
        self.assertEqual(self.dptId.main, "9")

    def test_sub(self):
        self.assertEqual(self.dptId.sub, "003")

    def test_generic(self):
        self.assertEqual(self.dptId.generic, DPTID("9.xxx"))

    def test_isGeneric(self):
        self.assertEqual(self.dptId.isGeneric(), False)
        self.assertEqual(self.dptId1.isGeneric(), True)

