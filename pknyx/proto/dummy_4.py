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


class LightsFB(FunctionalBlock):

    # Datapoints (= Group Objects) definition
    DP_01 = dict(name="lights_annexe", dptId="1.001", default="Off", access="output")

    GO_01 = dict(dp="lights_annexe", flags="CWTU", priority="low")

    DESC = "Lumières"

class Lights(Device):
    FB_01 = dict(cls=LightsFB, name="lights_fb", desc="lights fb")

    LNK_01 = dict(fb="lights_fb", dp="lights_annexe", gad="6/0/8")
    LNK_01a = dict(fb="lights_fb", dp="lights_annexe", gad="6/1/8")

ets = ETS()  # Borg
ets._gadMap = GAD_MAP

lights = Lights("1.1.1")

ets.register(lights)

ets.printGroat(lights,by="gad")
print()
print()
ets.printGroat(lights,by="go")
print()
print()

if __name__ == '__main__':
    lights.start()
    while True:
        try:
            time.sleep(9999)
        except KeyboardInterrupt:
            lights.stop()
            break
