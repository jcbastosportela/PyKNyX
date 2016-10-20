# -*- coding: utf-8 -*-

from pknyx.core.groupMonitor import *
import unittest

# Mute logger
from pknyx.services.logger import logging
logger = logging.getLogger(__name__)
logger.root.setLevel(logging.ERROR)


class GroupMonitorTestCase(unittest.TestCase):

    def setUp(self):
        self.group = Group("1/1/1", None)

    def tearDown(self):
        pass

    def test_display(self):
        print(repr(self.group))
        print(self.group)

    def test_constructor(self):
        pass

