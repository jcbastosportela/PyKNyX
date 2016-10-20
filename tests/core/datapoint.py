# -*- coding: utf-8 -*-

from pknyx.core.datapoint import *
import unittest

# Mute logger
logger.root.setLevel(logging.ERROR)


class DPTestCase(unittest.TestCase):

    def setUp(self):
        self.dp = Datapoint(self, name="dp", access="output", dptId="1.xxx", default=0.)

    def tearDown(self):
        pass

    def test_display(self):
        print(repr(self.dp))
        print(self.dp)

    def test_constructor(self):
        with self.assertRaises(DatapointValueError):
            DP = dict(name="dp", access="outpu", dptId="1.xxx", default=0.)
            Datapoint(self, **DP)

