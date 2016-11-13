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

Runs a Layer2 driver for multicasting

Implements
==========

 - B{UDPTransceiver}
 - B{UDPTransceiverValueError}

Documentation
=============

The UDPTransceiver uses the local address as returned by socket.gethostbyname(socket.gethostname()).
If the hostname is binded to the loopback interface (lo), then, all datas will only be sent/received on this interface.
You may need to configure this in /etc/hosts.

Usage
=====

@author: Frédéric Mantegazza
@copyright: (C) 2013-2015 Frédéric Mantegazza
@license: GPL

@todo: run transmitter and receiver in a simple threaded method, instead of a complete class thread.
"""


import time
import threading
import socket

from pknyx.common.exception import PKNyXValueError
from pknyx.services.logger import logging; logger = logging.getLogger(__name__)
from pknyx.stack.result import Result
from pknyx.stack.priority import Priority
from pknyx.stack.priorityQueue import PriorityQueue
from pknyx.stack.multicastSocket import MulticastSocketReceive, MulticastSocketTransmit
from pknyx.stack.layer2.l_dataServiceBase import L_DataServiceBroadcast
from pknyx.stack.knxnetip.knxNetIPHeader import KNXnetIPHeader, KNXnetIPHeaderValueError
from pknyx.stack.cemi.cemiLData import CEMILData, CEMIValueError
from pknyx.stack.layer2.l_dataService import PRIORITY_DISTRIBUTION


class UDPTransceiverValueError(PKNyXValueError):
    """
    """


class UDPTransceiver(L_DataServiceBroadcast):
    """ UDPTransceiver class

    @ivar _mcastAddr:
    @type _mcastAddr:

    @ivar _mcastPort:
    @type _mcastPort:

    @ivar _receiver: multicast receiver loop
    @type _receiver: L{Thread<threading>}

    @ivar _transmitter: multicast transmitter loop
    @type _transmitter: L{Thread<threading>}
    """
    def __init__(self, ets, mcastAddr="224.0.23.12", mcastPort=3671):
        """

        @param mcastAddr: multicast address to bind to
        @type mcastAddr: str

        @param mcastPort: multicast port to bind to
        @type mcastPort: str

        raise UDPTransceiverValueError:
        """
        super(UDPTransceiver, self).__init__(ets)

        self._mcastAddr = mcastAddr
        self._mcastPort = mcastPort

        localAddr = socket.gethostbyname(socket.gethostname())
        self._transmitterSock = MulticastSocketTransmit(localAddr, 0, mcastAddr, mcastPort)
        self._receiverSock = MulticastSocketReceive(localAddr, self._transmitterSock.localPort, mcastAddr, mcastPort)
        self._queue = PriorityQueue(PRIORITY_DISTRIBUTION)


        # Create transmitter and receiver threads
        self._receiver = threading.Thread(target=self._receiverLoop, name="UDP receiver")
        self._receiver.setDaemon(True)
        self._transmitter = threading.Thread(target=self._transmitterLoop, name="UDP transmitter")
        self._transmitter.setDaemon(True)

    @property
    def mcastAddr(self):
        return self._mcastAddr

    @property
    def mcastPort(self):
        return self._mcastPort

    @property
    def localAddr(self):
        return self._receiverSock.localAddr

    @property
    def localPort(self):
        return self._receiverSock.localPort

    def _receiverLoop(self):
        """
        """
        logger.trace("UDPTransceiver._receiverLoop()")

        while self._running:
            try:
                inFrame, (fromAddr, fromPort) = self._receiverSock.receive()
                logger.debug("UDPTransceiver._receiverLoop(): inFrame=%s (%s, %d)" % (repr(inFrame), fromAddr, fromPort))
                if fromAddr == self._transmitterSock.localAddress and fromPort == self._transmitterSock.localPort:
                    continue # we got our own packet
                inFrame = bytearray(inFrame)
                try:
                    header = KNXnetIPHeader(inFrame)
                except KNXnetIPHeaderValueError:
                    logger.exception("UDPTransceiver._receiverLoop()")
                    continue
                logger.debug("UDPTransceiver._receiverLoop(): KNXnetIP header=%s" % repr(header))

                frame = inFrame[KNXnetIPHeader.HEADER_SIZE:]
                logger.debug("UDPTransceiver._receiverLoop(): frame=%s" % repr(frame))
                try:
                    cEMI = CEMILData(frame)
                except CEMIValueError:
                    logger.exception("UDPTransceiver._receiverLoop()")
                    continue
                logger.debug("UDPTransceiver._receiverLoop(): cEMI=%s" % cEMI)

                self.dataReq(cEMI)

            except socket.timeout:
                pass

            except:
                logger.exception("UDPTransceiver._receiverLoop()")

        logger.trace("UDPTransceiver._receiverLoop(): ended")

    def dataInd(self, cEMI):
        self._queue.add(cEMI, cEMI.priority)

    def _transmitterLoop(self):
        """
        """
        logger.trace("UDPTransceiver._transmitterLoop()")

        while self._running:
            try:
                cEMI = self._queue.remove()
                if cEMI is None:
                    return

                logger.debug("UDPTransceiver._transmitterLoop(): frame=%s" % repr(cEMI))

                cEMIFrame = cEMI.frame
                cEMIRawFrame = cEMIFrame.raw
                header = KNXnetIPHeader(service=KNXnetIPHeader.ROUTING_IND, serviceLength=len(cEMIRawFrame))
                frame = header.frame + cEMIRawFrame
                logger.debug("UDPTransceiver._transmitterLoop(): frame= %s" % repr(frame))

                self._transmitterSock.transmit(frame)

            except Exception:
                logger.exception("UDPTransceiver._transmitterLoop()")

        logger.trace("UDPTransceiver._transmitterLoop(): ended")

    def start(self):
        """
        """
        logger.trace("UDPTransceiver.start()")

        self._running = True
        self._receiver.start()
        self._transmitter.start()

    def stop(self):
        """
        """
        logger.trace("UDPTransceiver.stop()")

        self._running = False
        self._queue.add(None,Priority('system'))
        self._transmitterSock.close()
        self._receiverSock.close()

