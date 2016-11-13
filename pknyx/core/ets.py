# -*- coding: utf-8 -*-

""" Python KNX framework

License
=======

 - B{pKNyX} (U{http://www.pknyx.org}) is Copyright:
  - (C) 2013-2015 Frédéric Mantegazza

This program is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation; either version 2 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program; if not, write to the Free Software
Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
or see:

 - U{http://www.gnu.org/licenses/gpl.html}

Module purpose
==============

ETS management

Implements
==========

 - B{ETS}

Documentation
=============

Usage
=====

@author: Frédéric Mantegazza
@copyright: (C) 2013-2015 Frédéric Mantegazza
@license: GPL
"""

import six
import threading

from pknyx.common.exception import PKNyXValueError
from pknyx.common.singleton import Singleton
from pknyx.services.logger import logging; logger = logging.getLogger(__name__)
from pknyx.stack.flags import Flags
from pknyx.stack.priority import Priority
from pknyx.stack.individualAddress import IndividualAddress
from pknyx.stack.groupAddress import GroupAddress
from pknyx.services.scheduler import Scheduler
from pknyx.services.notifier import Notifier
from pknyx.services.groupAddressTableMapper import GroupAddressTableMapper
from pknyx.stack.priorityQueue import PriorityQueue
from pknyx.stack.layer2.l_dataService import PRIORITY_DISTRIBUTION
from pknyx.stack.transceiver.udpTransceiver import UDPTransceiver


class ETSValueError(PKNyXValueError):
    """
    """

class ETS(threading.Thread):
    """ ETS class

    @ivar _devices: registered devices
    @type _devices: list of L{Device<pknyx.core.device>}

    @ivar _layer2: registered transports
    @type _devices: list of L{L_DataServiceBase<pknyx.stack.layer2.l_dataServiceBase>}

    @ivar _running: flag whether ETS has been started
    @type _devices: bool

    raise ETSValueError:
    """
    _running = False

    def __init__(self, addr, addrRange=-1,
                 transCls=UDPTransceiver,
                 transParams=dict(mcastAddr="224.0.23.12", mcastPort=3671)):
        """
        Set up the ETS stack.

        @param addr: the physical address of this stack (and possibly its sole device)
        """
        super(ETS, self).__init__()
        self._devices = set()
        self._layer2 = set()
        self._addr = addr
        self._addrNum = addrRange
        self._addrAlloc = addr
        self._queue = PriorityQueue(PRIORITY_DISTRIBUTION)

        self._scheduler = Scheduler()
        self.setDaemon(True)
        if transCls is None:
            self._tc = None
        else:
            self._tc = transCls(self, **transParams)
        #self.addLayer2(self._tc)


    def allocAddress(self):
        """
        Return a new physical address for a device.
        """
        if self._addrNum == -1:
            logger.info("Allocate ETS addr %s to device", self._addr)
            self._addrNum = 0
            return self._addr
        if self._addrNum == 0:
            raise ETSValueError("No free addresses")
        self._addrNum -= 1
        self._addrAlloc += 1
        logger.info("Allocate new ETS addr %s to device", self._addrAlloc)
        return self._addrAlloc

    @property
    def addr(self):
        return self._addr

    @property
    def gadMap(self):
        return self._gadMap

    @property
    def buildingMap(self):
        return self._buildingMap

    def addLayer2(self, layer2):
        self._layer2.add(layer2)
        if self._running:
            layer2.start()

    def register(self, device, buildingMap='root'):
        """
        Register a device

        This method registers pending scheduler/notifier jobs of all FunctionalBlock of the Device.

        @param device: device to register
        @type device: L{Device<pknyx.core.device>}
        """
        self._devices.add(device)

        for fb in device.fb.values():

            # Register pending scheduler/notifier jobs
            Scheduler().doRegisterJobs(fb)
            Notifier().doRegisterJobs(fb)

        for fb_, dp, gad in device.lnk:

            # Retrieve FunctionalBlock from device
            try:
                fb = device.fb[fb_]

            except KeyError:
                raise ETSValueError("unregistered functional block (%s)" % fb_)

            # Retrieve GroupObject from FunctionalBlock
            try:
                groupObject = fb.go[dp]

            except KeyError:
                raise ETSValueError("no Group Object associated with this datapoint (%s)" % dp)

            # Get GroupAddress
            if not isinstance(gad, GroupAddress):
                gad = GroupAddress(gad)

            # Ask the group data service to subscribe this GroupObject to the given gad
            # In return, get the created group
            group = device.stack.agds.subscribe(gad, groupObject)

            # If not already done, set the GroupObject group. This group will be used when the GroupObject wants to
            # communicate on the bus. This mimics the S flag of ETS real application.
            # @todo: find a better way
            if groupObject.group is None:
                groupObject.group = group

        if self._running:
            device.start()

    def putFrame(self, l2, cEMI):
        """
        Add a frame to be processed.

        @param cEMI:
        @type cEMI:
        """
        logger.debug("L_DataService.putInFrame(): cEMI=%s" % cEMI)

        # Get priority from cEMI
        priority = cEMI.priority

        # Add to inQueue and notify inQueue handler
        self._queue.add((l2,cEMI), priority)

    def start(self):
        if self._running:
            return
        self._queue = PriorityQueue(PRIORITY_DISTRIBUTION) # clean start
        super(ETS,self).start()

    def run(self):
        self._running = True
        try:
            for dev in self._layer2:
                dev.start()
            for dev in self._devices:
                dev.start()
            self._scheduler.start()
            while self._running:
                msg = self._queue.remove()
                if msg is None:
                    return
                l2,cEMI = msg
                self.processFrame(l2,cEMI)
        except Exception:
            logger.exception("ETS main loop")
        finally:
            self._running = False

    def stop(self):
        self._running = False
        self._scheduler.stop()
        self._queue.add(None,Priority('system'))
        for dev in self._devices:
            dev.stop()
        for dev in self._layer2:
            dev.stop()

    def processFrame(self, l2, cEMI):
        """
        Forward the frame @cEMI, received from layer2 device @l2, to all
        other eligible interfaces.
        """

        logger.trace("recv: get %s from %s", cEMI, l2)
        destAddr = cEMI.destinationAddress

        hopCount = cEMI.hopCount
        if hopCount == 7:
            # Refuse to transmit any packet with hopcount=7.
            # They may cause endlessly-looping packets. A multicast storm is
            # bad enough when something is misconfigured.
            cEMI.hopCount = hopCount = 6
            cEMI_b = cEMI
        elif l2.hop:
            # Decrement the hopcount if the packet arrives at one broadcast 
            # Layer2 and then gets re-broadcast. If zero, discard.
            if hopCount:
                cEMI_b = cEMI.copy()
                cEMI.b.hopCount = hopCount-1
            else:
                cEMI_b = None
        else:
            cEMI_b = cEMI
        if isinstance(destAddr, GroupAddress):
            r = 'wantsGroupFrame'
            may_force = False
        elif isinstance(destAddr, IndividualAddress):
            r = 'wantsIndividualFrame'
            may_force = True
        else:
            logger.warning("recv %s: unsupported destination address type (%s)", l2, repr(destAddr))
            return
        done = skipped = False
        for dev in self._layer2:
            if l2 == dev:
                continue
            cEMI_x = cEMI_b if dev.hop else cEMI
            if not cEMI_x:
                skipped = True
            elif getattr(dev,r)(cEMI):
                dev.dataInd(cEMI)
                done = True
        if may_force and not done:
            # We never saw this address. Send to every broadcast device.
            for dev in self._layer2:
                if l2 == dev:
                    continue
                cEMI_x = cEMI_b if dev.hop else cEMI
                if cEMI_x and getattr(dev,r)(cEMI, force=True):
                    done = True
            if done:
                logger.debug("recv %s: unknown destination address (%s)", repr(destAddr))
        if skipped:
            logger.debug("recv %s: not forwarded (hopcount zero): %s from %s", l2, cEMI)
        elif not done:
            logger.debug("recv %s: not sendable: %s from %s", l2, cEMI)


    def getGrOAT(self, device=None, by="gad", outFormatLevel=3):
        """ Build the Group Object Association Table
        """

        # Retrieve all bound gad
        gads = []
        if device is None:
            devices = self._devices
        else:
            devices = (device,)
        for dev in devices:
            for gad in dev.stack.agds.groups.keys():
                gads.append(GroupAddress(gad, outFormatLevel))
        gads.sort()  #reverse=True)

        output = "\n"

        if by == "gad":
            gadMapTable = GroupAddressTableMapper().table
            title = "%-34s %-30s %-30s %-10s %-10s %-10s" % ("GAD", "Datapoint", "Functional block", "DPTID", "Flags", "Priority")
            output += title
            output += "\n"
            output += len(title) * "-"
            output += "\n"
            gadMain = gadMiddle = gadSub = -1
            for gad in gads:
                if gadMain != gad.main:
                    index = "%d/-/-" % gad.main
                    name = gadMapTable.get(index,{'desc':''})
                    output +=  u"%2d %-33s\n" % (gad.main, name['desc'])
                    gadMain = gad.main
                    gadMiddle = gadSub = -1
                if gadMiddle != gad.middle:
                    index = "%d/%d/-" % (gad.main, gad.middle)
                    name = gadMapTable.get(index,{'desc':''})
                    output +=  u" ├── %2d %-27s\n" % (gad.middle, name['desc'])
                    gadMiddle = gad.middle
                    gadSub = -1
                index = "%d/%d/%d" % (gad.main, gad.middle, gad.sub)
                name = gadMapTable.get(index,{'desc':''})
                output +=  u" │    ├── %3d %-21s" % (gad.sub, name['desc'])
                gadSub = gad.sub

                i = 0
                for dev in devices:
                    groups = dev.stack.agds.groups
                    if gad.address not in groups:
                        continue
                    for go in groups[gad.address].listeners:
                        dp = go.datapoint
                        fb = dp.owner
                        if i:
                            output +=  u" │    │                            "
                        output +=  u"%-30s %-30s %-10s %-10s %-10s\n" % (dp.name, fb.name, dp.dptId, go.flags, go.priority)
                        i += 1

        elif by == "go":

            # Retrieve all groupObjects, not only bound ones
            # @todo: use buildingMap presentation
            mapByDP = {}
            title = "%-29s %-30s %-10s %-30s %-10s %-10s" % ("Functional block", "Datapoint", "DPTID", "GAD", "Flags", "Priority")
            output +=  title
            output += "\n"
            output +=  len(title) * "-"
            output += "\n"
            for dev in devices:
                for fb in dev.fb.values():
                    #output +=  "%-30s" % fb.name
                    for i, go in enumerate(fb.go.values()):
                        output +=  "%-30s" % ("" if i else fb.name)
                        dp = go.datapoint
                        gads_ = set()
                        groups = dev.stack.agds.groups
                        for gad in gads:
                            if gad.address not in groups:
                                continue
                            if go in groups[gad.address].listeners:
                                gads_.add(gad.address)
                        output +=  "%-30s %-10s %-30s %-10s %-10s\n" % (go.name, dp.dptId, ", ".join(gads_), go.flags, go.priority)

        else:
            raise ETSValueError("by param. must be in ('gad', 'dp')")

        return output

    def printGroat(self, *a,**k):
        print(self.getGrOAT(*a,**k))
        
    def mainLoop(self):
        self.start()
        try:
            while True:
                time.sleep(9999)
        except KeyboardInterrupt:
            pass
        finally:
            self._
            self.stop()

