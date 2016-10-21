# -*- coding: utf-8 -*-

from pknyx.services.scheduler import *
import time
import unittest
from pknyx.services.logger import _setup; _setup()

scheduler = Scheduler()

# Mute logger
from pknyx.services.logger import logging
logger = logging.getLogger(__name__)
logging.getLogger("pknyx").setLevel(logging.ERROR)

class SomeClass(object):
    runs = 0
    @scheduler.every(seconds=0.3)
    def again(self):
        self.runs += 1

class SchedulerTestCase(unittest.TestCase):

    def setUp(self):
        self.sched = Scheduler()
        self.sched.start()

    def tearDown(self):
        self.sched.stop()

    def test_register(self):
        some_obj = SomeClass()
        self.sched.doRegisterJobs(some_obj)
        time.sleep(1)
        assert some_obj.runs

