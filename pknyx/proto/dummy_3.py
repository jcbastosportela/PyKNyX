# -*- coding: utf-8 -*-

from __future__ import print_function

import time

from pknyx.api import Device, FunctionalBlock
from pknyx.core.ets import ETS

GAD_MAP = {1: {'root': "heating",
               1: {'root': "setpoint",
                   1: "living",
                   2: "bedroom 1",
                   3: "bedroom 2",
                   4: "bedroom 3"
                  },
               2: {'root': "temperature",
                   1: "living",
                   2: "bedroom 1",
                   3: "bedroom 2",
                   4: "bedroom 3"
                  }
              },
           2: {'root': "lights",
               1: {'root': None,
                   1: 'living',
                 },
               2: {'root': "etage",
                   1: None,
                   2: "bedroom 1"
                 }
              }
          }


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

ets = ETS()  # Borg
ets._gadMap = GAD_MAP

ets.register(dev1)
ets.register(dev2)
ets.weave(dev1)
ets.weave(dev2)

ets.printGroat(dev1,by="gad")
ets.printGroat(dev2,by="gad")
print()
print()
ets.printGroat(dev1,by="go")
ets.printGroat(dev2,by="go")
print()
print()

if __name__ == '__main__':
    dev1.start()
    dev2.start()
    while True:
        try:
            time.sleep(9999)
        except KeyboardInterrupt:
            dev1.stop()
            dev2.stop()
            break
