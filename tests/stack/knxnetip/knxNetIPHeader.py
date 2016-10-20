# -*- coding: utf-8 -*-

from pknyx.stack.knxnetip.knxNetIPHeader import *
import unittest

# Mute logger
from pknyx.services.logger import logging
logger = logging.getLogger(__name__)
logger.root.setLevel(logging.ERROR)


class KNXnetIPHeaderTestCase(unittest.TestCase):

    def setUp(self):
        self._header1 = KNXnetIPHeader(frame="\x06\x10\x05\x30\x00\x11\x29\x00\xbc\xd0\x11\x0e\x19\x02\x01\x00\x80")
        data = "\x29\x00\xbc\xd0\x11\x0e\x19\x02\x01\x00\x80\x00"
        self._header2 = KNXnetIPHeader(service=KNXnetIPHeader.ROUTING_IND, serviceLength=len(data))

    def tearDown(self):
        pass

    def test_constructor(self):
        with self.assertRaises(KNXnetIPHeaderValueError):
            KNXnetIPHeader(frame="\x06\x10\x05\x30\x00")  # frame length
        with self.assertRaises(KNXnetIPHeaderValueError):
            KNXnetIPHeader(frame="\x05\x10\x05\x30\x00\x11\x29\x00\xbc\xd0\x11\x0e\x19\x02\x01\x00\x80")  # header size
        with self.assertRaises(KNXnetIPHeaderValueError):
            KNXnetIPHeader(frame="\x06\x11\x05\x30\x00\x11\x29\x00\xbc\xd0\x11\x0e\x19\x02\x01\x00\x80")  # protocol version
        with self.assertRaises(KNXnetIPHeaderValueError):
            KNXnetIPHeader(frame="\x06\x10\xff\xff\x00\x11\x29\x00\xbc\xd0\x11\x0e\x19\x02\x01\x00\x80")  # service
        with self.assertRaises(KNXnetIPHeaderValueError):
            KNXnetIPHeader(frame="\x06\x10\x05\x30\x00\x10\x29\x00\xbc\xd0\x11\x0e\x19\x02\x01\x00\x80")  # total length

    def test_service(self):
        self.assertEqual(self._header1.service, KNXnetIPHeader.ROUTING_IND)
        self.assertEqual(self._header2.service, KNXnetIPHeader.ROUTING_IND)

    def test_totalSize(self):
        self.assertEqual(self._header1.totalSize, 17)
        self.assertEqual(self._header2.totalSize, 18)

    def test_byteArray(self):
        self.assertEqual(self._header1.frame, "\x06\x10\x05\x30\x00\x11")
        self.assertEqual(self._header2.frame, "\x06\x10\x05\x30\x00\x12")

    def test_serviceName(self):
        self.assertEqual(self._header1.serviceName, "routing.ind")
        self.assertEqual(self._header2.serviceName, "routing.ind")
