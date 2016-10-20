# -*- coding: utf-8 -*-

from pknyx.plugins.mail import *
import unittest

# Mute logger
logger.root.setLevel(logging.ERROR)


class MUATestCase(unittest.TestCase):

    def setUp(self):
        self.mua = MUA(smtp="localhost", subject="MUATestCase", to="pknyx@pknyx.org", from_="pknyx@pknyx.org")

    def tearDown(self):
        pass

    def test_send(self):
        self.mua.send("This is a test")
        mua = MUA("localhost")
        with self.assertRaises(MUAValueError):
            mua.send("Error")

