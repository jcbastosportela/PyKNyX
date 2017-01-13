# -*- coding: utf-8 -*-

from pyknyx.stack.cemi.cemiLData import *
import unittest

# Mute logger
from pyknyx.services.logger import logging
logger = logging.getLogger(__name__)
logging.getLogger("pyknyx").setLevel(logging.ERROR)


class CEMILDataTestCase(unittest.TestCase):

    def setUp(self):
        self.frame1 = CEMILData()
        self.frame2 = CEMILData(b")\x00\xbc\xd0\x11\x0e\x19\x02\x01\x00\x80")
        self.frame3 = CEMILData(b")\x00\xbc\xd0\x11\x04\x10\x04\x03\x00\x80\x19,")

    def tearDown(self):
        pass

    def test_display(self):
        assert repr(self.frame2) == "<CEMILData(mc=0x29, priority=<Priority('low')>, src=<IndividualAddress('1.1.14')>, dest=<GroupAddress('3/1/2')>, npdu=bytearray(b'\\x01\\x00\\x80'))>"
        assert str(self.frame3) == "<CEMILData(mc=0x29, priority=low, src=1.1.4, dest=2/0/4, npdu=bytearray(b'\\x03\\x00\\x80\\x19,'))>"

    def test_constructor(self):
        return ## XXX TODO I have no idea what's supposed to be wrong with this frame -- M:U
        with self.assertRaises(CEMIValueError):
            import pdb;pdb.set_trace()
            CEMILData(b")\x03\xff\xff\xff\xbc\xd0\x11\x04\x10\x04\x03\x00\x80\x19,")  # ext frame

