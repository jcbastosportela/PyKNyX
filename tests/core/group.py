# -*- coding: utf-8 -*-

from pknyx.core.group import *
import unittest

# Mute logger
logger.root.setLevel(logging.ERROR)


class GroupTestCase(unittest.TestCase):

    def setUp(self):
        self.group = Group("1/1/1", None)

    def tearDown(self):
        pass

    def test_display(self):
        print(repr(self.group))
        print(self.group)

    def test_constructor(self):
        pass

