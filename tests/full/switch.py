# -*- coding: utf-8 -*-

from pprint import pprint

from pknyx.api import Device, FunctionalBlock, notify
from pknyx.core.ets import ETS
from pknyx.tools.deviceRunner import *
import unittest

# Mute logger
from pknyx.services.logger import logging
logger = logging.getLogger(__name__)
logging.getLogger("pknyx").setLevel(logging.ERROR)


# A toggle button
class ToggleFB(FunctionalBlock):

    # Datapoints (= Group Objects) definition
    DP_01 = dict(name="change", dptId="1.001", default="Off", access="output")
    DP_02 = dict(name="status", dptId="1.001", default="Off", access="input")
    GO_01 = dict(dp="change", flags="CT", priority="low")
    GO_02 = dict(dp="status", flags="CWUI", priority="low")
    DESC = "ToggleFB"

class ActorFB(FunctionalBlock):
    DP_01 = dict(name="change", dptId="1.001", default="Off", access="input")
    DP_02 = dict(name="status", dptId="1.001", default="Off", access="output")
    GO_01 = dict(dp="change", flags="CW", priority="low")
    GO_02 = dict(dp="status", flags="CRT", priority="low")
    DESC = "ActorFB"

    _current = None

    @notify.datapoint(dp="change", condition="change")
    def stateChanged(self, event):
        if event['newValue'] == "On":
            self.on = True
        else:
            self.on = False

    @property
    def on(self):
        return self.dp["status"].value == "On"
    @on.setter
    def on(self, value):
        self._current = value
        if value:
            self.dp["status"].value = "On"
        else:
            self.dp["status"].value = "Off"


class Toggle(Device):
    FB_01 = dict(cls=ToggleFB, name="toggle_fb", desc="binary input")

    LNK_01 = dict(fb="toggle_fb", dp="change", gad="1/1/1")
    LNK_02 = dict(fb="toggle_fb", dp="status", gad="1/2/1")

    def set(self, value):
        self.fb["toggle_fb"].dp["change"].value = "On" if value else "Off"
    @property
    def status(self):
        return self.fb["toggle_fb"].dp["status"].value == "On"

class Actor(Device):
    FB_01 = dict(cls=ActorFB, name="actor_fb", desc="binary output")

    LNK_01 = dict(fb="actor_fb", dp="change", gad="1/1/1")
    LNK_02 = dict(fb="actor_fb", dp="status", gad="1/2/1")

class SwitchTestCase(unittest.TestCase):

    def setUp(self):
        self.ets = ETS("1.2.0", transCls=None)
        self.actor = Actor(self.ets, "1.2.3")
        self.toggle = Toggle(self.ets, "1.2.4")
        self.ets.start()

    def tearDown(self):
        self.ets.stop()

    def test_switch(self):
        afb = self.actor.fb["actor_fb"]
        assert afb._current is None
        time.sleep(0.5)
        logger.debug("Set TRUE")
        self.toggle.set(True)
        time.sleep(0.5)
        assert afb._current is True
        assert self.toggle.status
        logger.debug("Set FALSE")
        self.toggle.set(False)
        time.sleep(0.5)
        assert afb._current is False
        assert not self.toggle.status

