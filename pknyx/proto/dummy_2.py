# -*- coding: utf-8 -*-

from __future__ import print_function

from pprint import pprint

from pknyx.api import Device, FunctionalBlock
from pknyx.core.ets import ETS

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
    FB_01 = dict(cls=DevFB, name="dev_1", desc="weather fb 1")

    LNK_01 = dict(fb="dev_1", dp="dp_1", gad="1/1/1")
    LNK_01a = dict(fb="dev_1", dp="dp_1", gad="2/1/1")
    LNK_02 = dict(fb="dev_1", dp="dp_2", gad="1/1/2")
    LNK_03 = dict(fb="dev_1", dp="dp_3", gad="1/1/3")
    LNK_04 = dict(fb="dev_1", dp="dp_4", gad="1/1/4")

class Dev2(Device):
    FB_01 = dict(cls=DevFB, name="dev_2", desc="weather fb 2")

    LNK_01 = dict(fb="dev_2", dp="dp_1", gad="1/2/1")
    LNK_02 = dict(fb="dev_2", dp="dp_2", gad="1/2/2")
    LNK_02a = dict(fb="dev_2", dp="dp_2", gad="2/2/2")
    LNK_03 = dict(fb="dev_2", dp="dp_3", gad="1/1/3")
    #LNK_04 = dict(fb="dev_2", dp="dp_4", gad="1/1/4")

# TODO?
GAD_MAP = {1: {'name': "heating",
               1: {'name': "setpoint",
                   1: "living",
                   2: "bedroom 1",
                   3: "bedroom 2",
                   4: "bedroom 3",
                   },
               2: {'name': "temperature",
                   1: "living",
                   2: "bedroom 1",
                   3: "bedroom 2",
                   4: "bedroom 3",
                   },
               },
           2: {'name': "lights",
               1: {'name': None,
                   1: 'living',
                   },
               2: {'name': "etage",
                   1: None,
                   2: "bedroom 1",
                   },
               }
           }

def main():

    ets = ETS("7.9.99")  # Borg
    ets._gadMap = GAD_MAP

    dev1 = Dev1(ets, "1.1.1")
    dev2 = Dev2(ets, "1.1.2")

    ets.printGroat(by="gad")
    print()
    ets.printGroat(by="go")

if __name__ == "__main__":
    main()
