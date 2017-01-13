# -*- coding: utf-8 -*-

""" Python KNX framework

License
=======

 - B{pKNyX} (U{http://www.pyknyx.org}) is Copyright:
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

Group data service management

Implements
==========

 - B{GroupMonitorValueError}
 - B{GroupMonitor}

Documentation
=============

A B{GroupMonitor} is a special L{Group<pyknyx.core.group>} which handles all group addresses. Unlink normal
L{Group<pyknyx.core.group>}, it can't send anything on the bus.

Usage
=====

@author: Frédéric Mantegazza
@copyright: (C) 2013-2015 Frédéric Mantegazza
@license: GPL
"""

from pyknyx.common.exception import PKNyXValueError
from pyknyx.services.logger import logging; logger = logging.getLogger(__name__)
from pyknyx.stack.layer7.a_groupDataListener import A_GroupDataListener


class GroupMonitorValueError(PKNyXValueError):
    """
    """


class GroupMonitor(A_GroupDataListener):
    """ GroupMonitor class

    This special group monitors all group adress. It can't send anything on the bus, only receive.

    @ivar _agds: Application Group Data Service object
    @type _agds: L{A_GroupDataService}

    @ivar _listeners: Listeners bound to the group handled GAD
    @type _listeners: set of L{GroupObject<pyknyx.core.groupObject>}
    """
    def __init__(self, agds):
        """ Init the GroupMonitor object

        @param agds: Application Group Data Service object
        @type agds: L{A_GroupDataService}

        raise GroupValueError:
        """
        super(GroupMonitor, self).__init__()

        self._agds = agds

        self._listeners = set()

    def __repr__(self):
        return "<GroupMonitor()>" % self._gad

    def __str__(self):
        return "<GroupMonitor()>" % self._gad

    def groupValueWriteInd(self, src, gad, priority, data):
        logger.debug("GroupMonitor.groupValueWriteInd(): src=%s, gad=%s, priority=%s, data=%s" % \
                       (src, gad, priority, repr(data)))
        for listener in self._listeners:
            try:
                listener.onWrite(src, gad, priority, data)
            except PKNyXValueError:
                logger.exception("GroupMonitor.groupValueWriteInd()")

    def groupValueReadInd(self, src, gad, priority):
        logger.debug("GroupMonitor.groupValueReadInd(): src=%s, gad=%s, priority=%s" % (src, gad, priority))
        for listener in self._listeners:
            try:
                listener.onRead(src, gad, priority)
            except PKNyXValueError:
                logger.exception("GroupMonitor.groupValueReadInd()")

    def groupValueReadCon(self, src, gad, priority, data):
        logger.debug("GroupMonitor.groupValueReadCon(): src=%s, gad=%s, priority=%s, data=%s" % \
                       (src, gad, priority, repr(data)))
        for listener in self._listeners:
            try:
                listener.onResponse(src, gad, priority, data)
            except PKNyXValueError:
                logger.exception("GroupMonitor.groupValueReadCon()")

    @property
    def listeners(self):
        return self._listeners

    def addListener(self, listener):
        """ Add a listener to this group

        The given listener is added to the listeners bound with the GAD handled by this group.

        @param listener: Listener
        @type listener: L{GroupMonitorListener<pyknyx.core.groupMonitorListener>}

        @todo: check listener type
        """
        self._listeners.add(listener)

