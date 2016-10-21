# -*- coding: utf-8 -*-

from pknyx.core.dptXlator.dpt import *
import unittest

# Mute logger
from pknyx.services.logger import logging
logger = logging.getLogger(__name__)
logging.getLogger("pknyx").setLevel(logging.ERROR)


class DPT_TestCase(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_display(self):
        pass

    def test_constructor(self):
        with self.assertRaises(DPTValueError):
            DPT("9.001", "Temperature", -273)

