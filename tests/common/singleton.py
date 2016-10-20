# -*- coding: utf-8 -*-

from pknyx.common.singleton import *
import unittest

# Mute logger
from pknyx.services.logger import logging; logger = logging.getLogger(__name__)
logger.root.setLevel(logging.ERROR)


@six.add_metaclass(Singleton)
class SingletonTest(object):
    pass

class SingletonTestCase(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_constructor(self):
        s1 = SingletonTest()
        s2 = SingletonTest()
        self.assertIs(s1, s2)

