# -*- coding: utf-8 -*-

from pknyx.core.dptXlator.dptXlatorBase import *
import unittest

# Mute logger
from pknyx.services.logger import logging
logger = logging.getLogger(__name__)
logger.root.setLevel(logging.ERROR)


class DPTXlatorBaseTestCase(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_display(self):
        pass

    def test_constructor(self):
        with self.assertRaises(DPTXlatorValueError):
            DPTXlatorBase("1.001", 0)
