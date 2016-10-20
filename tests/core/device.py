# -*- coding: utf-8 -*-

from pknyx.core.device import *
import unittest

# Mute logger
from pknyx.services.logger import logging
logger = logging.getLogger(__name__)
logger.root.setLevel(logging.ERROR)


class DeviceTestCase(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_constructor(self):
        pass

