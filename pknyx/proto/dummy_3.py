
import time

from pknyx.api import Device, Stack, ETS

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


class Dev(Device):

    # Datapoints (= Group Objects) definition
    DP_01 = dict(name="dp_1", dptId="1.001", flags="CWTU", priority="low", defaultValue=0.)
    DP_02 = dict(name="dp_2", dptId="1.001", flags="CWTU", priority="low", defaultValue=0.)
    DP_03 = dict(name="dp_3", dptId="1.001", flags="CWTU", priority="low", defaultValue=0.)
    DP_04 = dict(name="dp_4", dptId="1.001", flags="CWTU", priority="low", defaultValue=0.)

    DESC = "Truc bidule"


stack = Stack()   # Borg
ets = ETS(stack)  # Borg
ets.gadMap = GAD_MAP

dev1 = Dev(name="dev1", desc="Device 1", address="1.1.1")
dev2 = Dev(name="dev2", desc="Device 2", address="1.1.2")

ets.register(dev1)
ets.register(dev2)

ets.link(dev=dev1, dp="dp_1", gad=("1/1/1", "2/1/1"))
ets.link(dev=dev1, dp="dp_2", gad="1/1/2")
ets.link(dev=dev1, dp="dp_3", gad="1/1/3")
ets.link(dev=dev1, dp="dp_4", gad="1/1/4")

ets.link(dev=dev2, dp="dp_1", gad="1/2/1")
ets.link(dev=dev2, dp="dp_2", gad=("1/2/2", "2/2/2"))
ets.link(dev=dev2, dp="dp_3", gad="1/1/3")
#ets.link(dev=dev2, dp="dp_4", gad="1/1/4")

ets.printGroat(dev1,by="gad")
ets.printGroat(dev2,by="gad")
print
print
ets.printGroat(dev1,by="go")
ets.printGroat(dev2,by="go")
print
print

stack.start()
while True:
    try:
        time.sleep(0.1)
    except KeyboardInterrupt:
        stack.stop()
        break
