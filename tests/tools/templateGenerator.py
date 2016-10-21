# -*- coding: utf-8 -*-

from pknyx.tools.templateGenerator import *
import unittest

# Mute logger
from pknyx.services.logger import logging
logger = logging.getLogger(__name__)
logging.getLogger("pknyx").setLevel(logging.ERROR)


class TemplateGeneratorTestCase(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_constructor(self):
        pass

