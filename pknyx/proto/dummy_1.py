from pprint import pprint

from pknyx.api import Device, FunctionalBlock
from pknyx.core.ets import ETS

ets = ETS()

# Weather station class definition
class WeatherStationFB(FunctionalBlock):

    # Datapoints (= Group Objects) definition
    DP_01 = dict(name="temperature", dptId="9.001", default=0., access="output")
    DP_02 = dict(name="humidity", dptId="9.007", default=0., access="output")
    DP_03 = dict(name="wind_speed", dptId="9.005", default=0., access="output")
    DP_04 = dict(name="wind_alarm", dptId="1.005", default="No alarm", access="output")
    DP_05 = dict(name="wind_speed_limit", dptId="9.005", default=15., access="input")
    DP_06 = dict(name="wind_alarm_enable", dptId="1.003", default="Disable", access="input")

    GO_01 = dict(dp="temperature", flags="CRT", priority="low")
    GO_02 = dict(dp="humidity", flags="CRT", priority="low")
    GO_03 = dict(dp="wind_speed", flags="CRT", priority="low")
    GO_04 = dict(dp="wind_alarm", flags="CRT", priority="low")
    GO_05 = dict(dp="wind_speed_limit", flags="CWTU", priority="low")
    GO_06 = dict(dp="wind_alarm_enable", flags="CWTU", priority="low")

    DESC = "WeatherStation"

# Creation of the weather station device object
class WeatherStation(Device):
    FB_01 = dict(cls=WeatherStationFB, name="weather_fb", desc="weather fb")

    LNK_01 = dict(fb="weather_fb", dp="temperature", gad="1/1/1")
    LNK_02 = dict(fb="weather_fb", dp="humidity", gad="1/2/1")
    LNK_03 = dict(fb="weather_fb", dp="wind_speed", gad="1/3/1")
    LNK_04 = dict(fb="weather_fb", dp="wind_alarm", gad="1/4/1")
    LNK_05 = dict(fb="weather_fb", dp="wind_speed_limit", gad="1/5/1")
    LNK_06 = dict(fb="weather_fb", dp="wind_alarm_enable", gad="1/6/1")
station = WeatherStation("1.2.3")

# Linking weather station Datapoints to Group Addresses
ets.link(station)

ets.printGroat(station, by="gad")
ets.printGroat(station, by="go")
