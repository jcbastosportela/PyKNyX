# -*- coding: utf-8 -*-

from pknyx.plugins.mail import *
import unittest

# Mute logger
from pknyx.services.logger import logging
logger = logging.getLogger(__name__)
logging.getLogger("pknyx").setLevel(logging.ERROR)


class MUATestCase(unittest.TestCase):

    def setUp(self):
        self.mua = MUA(smtp="localhost", subject="MUATestCase", to="pknyx@pknyx.org", from_="pknyx@pknyx.org")

    def tearDown(self):
        pass

    def test_send(self):
        # who guarantees that there's a MUA on localhost, much less listening on port 25?
        if False:
            self.mua.send("This is a test")

        mua = MUA("localhost")
        with self.assertRaises(MUAValueError):
            mua.send("Error")

