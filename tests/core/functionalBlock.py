# -*- coding: utf-8 -*-

from pyknyx.core.functionalBlock import *
import unittest

# Mute logger
from pyknyx.services.logger import logging
logger = logging.getLogger(__name__)
logging.getLogger("pyknyx").setLevel(logging.ERROR)


class FunctionalBlockTestCase(unittest.TestCase):

    class TestFunctionalBlock(FunctionalBlock):
        DP_01 = dict(name="dp_01", access="output", dptId="9.001", default=19.)
        DP_02 = dict(name="dp_02", access="output", dptId="9.007", default=50.)
        DP_03 = dict(name="dp_03", access="output", dptId="9.005", default=0.)
        DP_04 = dict(name="dp_04",  access="output", dptId="1.005", default="No alarm")
        DP_05 = dict(name="dp_05",  access="input", dptId="9.005", default=15.)
        DP_06 = dict(name="dp_06", access="input", dptId="1.003", default="Disable")

        GO_01 = dict(dp="dp_01", flags="CRT", priority="low")
        GO_02 = dict(dp="dp_02", flags="CRT", priority="low")
        GO_03 = dict(dp="dp_03", flags="CRT", priority="low")
        GO_04 = dict(dp="dp_04", flags="CRT", priority="low")
        GO_05 = dict(dp="dp_05", flags="CWU", priority="low")
        GO_06 = dict(dp="dp_06", flags="CWU", priority="low")

        DESC = "Dummy description"

    def setUp(self):
        self.fb1 = FunctionalBlockTestCase.TestFunctionalBlock(dev="foo", name="test1")
        self.fb2 = FunctionalBlockTestCase.TestFunctionalBlock(dev="bar", name="test2", desc="pipo")

    def tearDown(self):
        pass

    def test_display(self):
        assert repr(self.fb1) == "<TestFunctionalBlock(foo, name='test1', desc='Dummy description')>"
        assert str(self.fb2) == "<TestFunctionalBlock(bar, 'test2')>"

    def test_constructor(self):
        pass

