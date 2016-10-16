# -*- coding: utf-8 -*-

from __future__ import print_function

from pprint import pprint

from pknyx.api import Device, FunctionalBlock
from pknyx.core.ets import ETS

ets = ETS()  # Borg

class DevFB(FunctionalBlock):

    # Datapoints (= Group Objects) definition
    DP_01 = dict(name="dp_1", dptId="1.001", default="Off", access="output")
    DP_02 = dict(name="dp_2", dptId="1.001", default="Off", access="output")
    DP_03 = dict(name="dp_3", dptId="1.001", default="Off", access="output")
    DP_04 = dict(name="dp_4", dptId="1.001", default="Off", access="output")

    GO_01 = dict(dp="dp_1", flags="CWTU", priority="low")
    GO_02 = dict(dp="dp_2", flags="CWTU", priority="low")
    GO_03 = dict(dp="dp_3", flags="CWTU", priority="low")
    GO_04 = dict(dp="dp_4", flags="CWTU", priority="low")

    DESC = "Truc bidule"

class Dev1(Device):
    FB_01 = dict(cls=DevFB, name="dev_fb", desc="weather fb")

    LNK_01 = dict(fb="dev_fb", dp="dp_1", gad="1/1/1")
    LNK_01a = dict(fb="dev_fb", dp="dp_1", gad="2/1/1")
    LNK_02 = dict(fb="dev_fb", dp="dp_2", gad="1/1/2")
    LNK_03 = dict(fb="dev_fb", dp="dp_3", gad="1/1/3")
    LNK_04 = dict(fb="dev_fb", dp="dp_4", gad="1/1/4")

class Dev2(Device):
    FB_01 = dict(cls=DevFB, name="dev_fb", desc="weather fb")

    LNK_01 = dict(fb="dev_fb", dp="dp_1", gad="1/2/1")
    LNK_02 = dict(fb="dev_fb", dp="dp_2", gad="1/2/2")
    LNK_02a = dict(fb="dev_fb", dp="dp_2", gad="2/2/2")
    LNK_03 = dict(fb="dev_fb", dp="dp_3", gad="1/1/3")
    #LNK_04 = dict(fb="dev_fb", dp="dp_4", gad="1/1/4")

dev1 = Dev1("1.1.1")
dev2 = Dev2("1.1.2")

ets.register(dev1)
ets.register(dev2)

# TODO?
ets._gadMap = {1: {'name': "heating",
                    1: {'name': "setpoint",
                        1: "living",
                        2: "bedroom 1",
                        3: "bedroom 2",
                        4: "bedroom 3"
                        },
                    2: {'name': "temperature",
                        1: "living",
                        2: "bedroom 1",
                        3: "bedroom 2",
                        4: "bedroom 3"
                        }
                    },
                2: {'name': "lights",
                    1: {'name': None,
                        1: 'living',
                       },
                    2: {'name': "etage",
                        1: None,
                        2: "bedroom 1"
                       }
                    }
                }

#ets.printGroat()
ets.printGroat(dev1,by="gad")
ets.printGroat(dev2,by="gad")
print()
print()
ets.printGroat(dev1,by="go")
ets.printGroat(dev2,by="go")
