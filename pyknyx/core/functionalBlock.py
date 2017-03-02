# -*- coding: utf-8 -*-

""" Python KNX framework

License
=======

 - B{PyKNyX} (U{https://github.com/knxd/pyknyx}) is Copyright:
  - © 2016-2017 Matthias Urlichs
  - PyKNyX is a fork of pKNyX
   - © 2013-2015 Frédéric Mantegazza

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

Application management

Implements
==========

 - B{FunctionalBlockValueError}
 - B{FunctionalBlock}

Documentation
=============

B{FunctionalBlock} is one of the most important object of B{PyKNyX} framework, after L{Datapoint<pyknyx.core.datapoint>}.

Usage
=====

@author: Frédéric Mantegazza
@copyright: (C) 2013-2015 Frédéric Mantegazza
@license: GPL
"""

from pyknyx.common.exception import PyKNyXValueError
from pyknyx.common.utils import reprStr
from pyknyx.common.frozenDict import FrozenDict
from pyknyx.services.logger import logging; logger = logging.getLogger(__name__)
from pyknyx.services.notifier import Notifier
from pyknyx.core.datapoint import Datapoint, DP
from pyknyx.core.groupObject import GroupObject, GO


class FunctionalBlockValueError(PyKNyXValueError):
    """
    """

class FB_DP(object):
    def __init__(self, fb,dp):
        self.fb = fb
        self.dp = dp

    def gen(self,obj):
        fb = obj.fb[self.fb.name]
        if isinstance(self.dp,str):
            return fb.go[self.dp]
        else:
            for val in fb.go.values():
                if val._factory.dp is self.dp:
                    return val
            else:
                raise KeyError("I could not find the GO for DP '%s' in FB '%s'"%(self.dp.name, fb.__class__.__name__))


class FB(object):
    """ FunctionalBlock factory
        
    This class collects arguments for instantiating a L{FunctionalBlock} when a
    L{Device} is created.

    Arguments are the same as L{FunctionalBlock}.
    """ 
    def __init__(self, cls, name=None, *args, **kwargs):
        """ Remember parameters for eventual instantiation of a L{Datapoint}.

        See B{FunctionalBlock.__init__} for parameters.
        """
        self.cls = cls
        self.name = name
        self.args = args
        self.kwargs = kwargs

    def __getattr__(self, key):
        """
        Required for LNK(fb_name.dp_name) to work
        """
        return FB_DP(self, getattr(self.cls,key))

    def gen(self, obj, name=None):
        """ Instantiate the funcional block.

        If no name is passed in here, the one used in creating this object
        is used as a fallback.

        @param owner: owner of the datapoint.
        @type owner: L{FunctionalBlock<pyknyx.core.functionalBloc>}

        @param name: name of the datapoint. 
        @type name: str
        """
        if self.name is not None:
            assert name is None or name == self.name
            name = self.name
        assert name, "A FunctionalBlock needs to be named"

        fb = self.cls(obj, name, *self.args, **self.kwargs)
        fb._factory = self # required for finding it in Link creation
        return fb


class FunctionalBlock(object):
    """ FunctionalBlock class

    The Datapoints of a FunctionalBlock must be defined in sub-classes, as class dict, and named B{DP_xxx}. They will be
    automatically instanciated as real L{Datapoint} objects, and added to the B{_datapoints} dict.

    Same for GroupObject.

    @ivar _name: name of the functional block
    @type _name: str

    @ivar _device: device
    @type _device: L{Device} instance

    @ivar _desc: description of the device
    @type _desc:str

    @ivar _params: additional user params
    @type _params: dict

    @ivar _datapoints: Datapoints exposed by this FunctionalBlock
    @type _datapoints: dict of L{Datapoint}

    @ivar _groupObjects: GroupObjects exposed by this FunctionalBlock
    @type _groupObjects: dict of L{GroupObject}
    """
    def __new__(cls, dev, name, *args, **kwargs):
        """ Init the class with all available types for this DPT
        """
        self = super(FunctionalBlock, cls).__new__(cls)
        self._name = name

        self._device = dev

        # Retrieve all parents classes, to get all objects defined there
        classes = cls.__mro__

        # objects named B{DP_xxx} or of type DP are treated as Datapoint and added to the B{_datapoints} dict
        datapoints = {}
        for cls_ in classes[::-1]:
            for key, value in cls_.__dict__.items():
                if key.startswith("DP_") and isinstance(value,dict):
                    assert 'name' in value, value
                    value = DP(**value)
                    key = value.name

                if isinstance(value, DP):
                    if value.name is None:
                        value.name = key
                    value = value.gen(self, key)
                    logger.debug("%s: new DP %s: %s", self, repr(key), value)
                    datapoints[key] = value
                elif key in datapoints and value is None:
                    logger.debug("%s: drop DP %s", self, repr(key))
                    del datapoints[key]

        self._datapoints = FrozenDict(datapoints)

        # If a Datapoint has Flags, auto-generate a GO for it as a shortcut
        groupObjects = {}
        for key, value in datapoints.items():
            if value.flags is not None:
                groupObjects[key] = GO(value._factory, flags=value.flags, priority=value.priority).gen(self)

        # objects named B{GO_xxx} or of type GO are treated as GroupObjects and added to the B{_groupObjects} dict
        for cls_ in classes[::-1]:
            for key, value in cls_.__dict__.items():
                if key.startswith("GO_") and isinstance(value, dict):
                    key = value.get('name',key)
                    value = GO(**value)

                if isinstance(value, GO):
                    value = value.gen(self)
                    key = value.datapoint.name
                    logger.debug("%s: new GO %s: %s", self, repr(key), value)
                    groupObjects[key] = value
                elif key in groupObjects and value is None:
                    logger.debug("%s: drop GO %s", self, repr(key))
                    del groupObjects[key]
        self._groupObjects = FrozenDict(groupObjects)

        try:
            self._desc = cls.__dict__["DESC"]
        except KeyError:
            logger.error("%s: missing DESCription", cls)
            self._desc = "FB"

        return self

    def __init__(self, dev, name, desc=None, params={}):
        """

        @param name: name of the device
        @type name: str

        @param desc: description of the device
        @type desc: str

        @param params: additional user params
        @type params: dict

        raise FunctionalBlockValueError:
        """
        super(FunctionalBlock, self).__init__()

        if desc is not None:
            self._desc = "%s::%s" % (self._desc, desc)

        self._params = params

        # Call for additional user init
        self.init()

    def __repr__(self):
        return "<%s(%s, name='%s', desc='%s')>" % (reprStr(self.__class__), self._device, self._name, self._desc)

    def __str__(self):
        return "<%s(%s, '%s')>" % (reprStr(self.__class__), self._device, self._name)

    def init(self):
        """ Additional user init
        """
        pass

    @property
    def name(self):
        return self._name

    @property
    def desc(self):
        return self._desc

    @property
    def device(self):
        return self._device

    @property
    def params(self):
        return self._params

    @property
    def dp(self):
        return self._datapoints

    @property
    def go(self):
        return self._groupObjects

    def notify(self, dp, oldValue, newValue):
        """ Notify the functional block of a datapoint value change

        The functional block must trigger all methods bound to this notification with xxx.notify.datapoint()

        @param dp: name of the datapoint which sent this notification
        @type dp: str

        @param oldValue: old value of the datapoint
        @type oldValue: depends on the datapoint DPT

        @param newValue: new value of the datapoint
        @type newValue: depends on the datapoint DPT

        @todo: use an Event as param
        """
        logger.debug("FunctionalBlock.notify(): dp=%s, oldValue=%s, newValue=%s" % (dp, oldValue, newValue))

        Notifier().datapointNotify(self, dp, oldValue, newValue)

