# -*- coding: utf-8 -*-

from pyknyx.services.groupAddressTableMapper import *
import unittest

# Mute logger
from pyknyx.services.logger import logging
logger = logging.getLogger(__name__)
logging.getLogger("pyknyx").setLevel(logging.ERROR)

GAD_MAP_TABLE = {"1/-/-": dict(name="light", desc="Lights (1/-/-)"),
                    "1/1/-": dict(name="light_cmd", desc="Commands (1/1/-)"),
                    "1/1/1": dict(name="light_cmd_test", desc="Test (1/1/1)"),
                    "1/2/-": dict(name="light_state", desc="States (1/2/-)"),
                    "1/2/1": dict(name="light_state_test", desc="Test (1/2/1)"),
                    "1/3/-": dict(name="light_delay", desc="Delays (1/3/-)"),
                    "1/3/1": dict(name="light_delay_test", desc="Test (1/3/1)"),
                }


class GroupAddressTableMapperTestCase(unittest.TestCase):

    def setUp(self):
        self._gadTableMapper = GroupAddressTableMapper()
        self._gadTableMapper.loadWith(GAD_MAP_TABLE)

    def tearDown(self):
        pass

    def test_table(self):
        self.assertEqual(self._gadTableMapper.table, GAD_MAP_TABLE)

    def test_isTableValid(self):
        TABLE_OK = {"1/1/1": dict(name="test 1", desc="Test (1/1/1)"),
                    "1/1/2": dict(name="test 2", desc="Test (1/1/2)")
                    }
        TABLE_WRONG = {"1/1/1": dict(name="test", desc="Test (1/1/1)"),
                        "1/1/2": dict(name="test", desc="Test (1/1/2)")
                        }
        self.assertEqual(self._gadTableMapper.isTableValid(TABLE_OK), True)
        self.assertEqual(self._gadTableMapper.isTableValid(TABLE_WRONG), False)

    def test_getGad(self):
        self.assertEqual(self._gadTableMapper.getGad("light"), "1/-/-")
        self.assertEqual(self._gadTableMapper.getGad("light_cmd"), "1/1/-")
        self.assertEqual(self._gadTableMapper.getGad("light_cmd_test"), "1/1/1")

    def test_getNickname(self):
        self.assertEqual(self._gadTableMapper.getNickname("1/-/-"), "light")
        self.assertEqual(self._gadTableMapper.getNickname("1/1/-"), "light_cmd")
        self.assertEqual(self._gadTableMapper.getNickname("1/1/1"), "light_cmd_test")

    def test_getDesc(self):
        self.assertEqual(self._gadTableMapper.getDesc("1/-/-"), "Lights (1/-/-)")
        self.assertEqual(self._gadTableMapper.getDesc("1/1/-"), "Commands (1/1/-)")
        self.assertEqual(self._gadTableMapper.getDesc("1/1/1"), "Test (1/1/1)")
        self.assertEqual(self._gadTableMapper.getDesc("light"), "Lights (1/-/-)")
        self.assertEqual(self._gadTableMapper.getDesc("light_cmd"), "Commands (1/1/-)")
        self.assertEqual(self._gadTableMapper.getDesc("light_cmd_test"), "Test (1/1/1)")

