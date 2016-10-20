# -*- coding: utf-8 -*-

from pknyx.core.dptXlator.dptXlatorFactory import *
import unittest

# Mute logger
logger.root.setLevel(logging.ERROR)

class DPTMainTypeMapperTestCase(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_constructor(self):
        class DummyClass(object):
            pass

        with self.assertRaises(DPTXlatorValueError):
            DPTMainTypeMapper("1.xxx", DummyClass, "Dummy")
        DPTMainTypeMapper("1.xxx", DPTXlatorBoolean, "Dummy")

class DPTXlatorFactoryObjectTestCase(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    #def test_constructor(self):
        #print DPTXlatorFactory().handledMainDPTIDs
