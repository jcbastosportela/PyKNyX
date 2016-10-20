# -*- coding: utf-8 -*-

from pknyx.stack.priority import *
import unittest

# Mute logger
from pknyx.services.logger import logging
logger = logging.getLogger(__name__)
logger.root.setLevel(logging.ERROR)


class PriorityTestCase(unittest.TestCase):

    def setUp(self):
        self.priority1 = Priority('system')
        self.priority2 = Priority('normal')
        self.priority3 = Priority('urgent')
        self.priority4 = Priority('low')
        self.priority5 = Priority(0x00)
        self.priority6 = Priority(0x01)
        self.priority7 = Priority(0x02)
        self.priority8 = Priority(0x03)

    def tearDown(self):
        pass

    def test_display(self):
        print(repr(self.priority1))
        print(self.priority1)

    def test_constructor(self):
        with self.assertRaises(PriorityValueError):
            Priority(-1)
        with self.assertRaises(PriorityValueError):
            Priority(4)
        with self.assertRaises(PriorityValueError):
            Priority('toto')

    def test_level(self):
        self.assertEqual(self.priority1.level, 0x00)
        self.assertEqual(self.priority2.level, 0x01)
        self.assertEqual(self.priority3.level, 0x02)
        self.assertEqual(self.priority4.level, 0x03)

    def test_name(self):
        self.assertEqual(self.priority5.name, 'system')
        self.assertEqual(self.priority6.name, 'normal')
        self.assertEqual(self.priority7.name, 'urgent')
        self.assertEqual(self.priority8.name, 'low')
