# -*- coding: utf-8 -*-

""" Python KNX framework

License
=======

 - B{PyKNyX} (U{http://www.pyknyx.org}) is Copyright:
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

Scheduler management

Implements
==========

 - B{Scheduler}
 - B{SchedulerValueError}

Documentation
=============

One of the nice feature of B{PyKNyX} is to be able to register some L{FunctionalBlock<pyknyx.core.functionalBlock>}
sub-classes methods to have them executed at specific times. For that, B{PyKNyX} uses the nice third-party module
U{APScheduler<http://pythonhosted.org/APScheduler>}.

The idea is to use the decorators syntax to register these methods

Unfortunally, a decorator can only wraps a function. But what we want is to register an instance method! How can it be
done, as we didn't instanciated the class yet?

Luckily, such classes are not directly instanciated by the user, but through the L{ETS<pyknyx.core.ets>} register()
method. So, here is how this registration is done.

Instead of directly using the APScheduler, the Scheduler class below provides the decorators we need, and maintains a
list of names of the decorated functions, in _pendingFuncs.

Then, when a new instance of the FunctionalBlock sub-class is created, in ets.register(), we call the
Scheduler.doRegisterJobs() method which tried to retrieve the bounded method matching one of the decorated functions.
If found, the method is registered in APScheduler.

Scheduler also adds a listener to be notified when a decorated method call fails to be run, so we can log it.

Usage
=====

@author: Frédéric Mantegazza
@copyright: (C) 2013-2015 Frédéric Mantegazza
@license: GPL
"""

import six
import traceback

from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.events import EVENT_JOB_ERROR,EVENT_JOB_MISSED

from pyknyx.common.exception import PyKNyXValueError
from pyknyx.common.singleton import Singleton
from pyknyx.services.logger import logging; logger = logging.getLogger(__name__)
from pyknyx.common.utils import func_name, meth_name,meth_self,meth_func

scheduler = None


class SchedulerValueError(PyKNyXValueError):
    """
    """

@six.add_metaclass(Singleton)
class Scheduler(object):
    """ Scheduler class

    @ivar _pendingFuncs:
    @type _pendingFuncs: list

    @ivar _apscheduler: real scheduler
    @type _apscheduler: APScheduler
    """

    TYPE_EVERY = "interval"
    TYPE_AT = "date"
    TYPE_CRON = "cron"

    _apscheduler = None

    def __init__(self, autoStart=False, type_=BackgroundScheduler):
        """ Init the Scheduler object

        @param autoStart: if True, automatically starts the scheduler
        @type autoStart: bool

        raise SchedulerValueError:
        """
        super(Scheduler, self).__init__()
        self._type = type_

        if autoStart:
            self.start()

    def _listener(self, event):
        """ APScheduler listener.

        This listener is called by APScheduler when executing jobs.

        It can be setup so only errors are triggered.
        """
        logger.debug("Scheduler._listener(): event=%s" % repr(event))

        if event.exception:
            message = "Scheduler._listener()\n" + "".join(traceback.format_tb(event.traceback)) + str(event.exception)
            logger.exception(message)

    @property
    def apscheduler(self):
        return self._apscheduler

    def _register(self, typ,func,kwargs):
        jobs = getattr(func,'_Sched', None)
        if jobs is None:
            jobs = []
            setattr(func,'_Sched', jobs)
        jobs.append((typ,kwargs))

    def every(self, **kwargs):
        """ Decorator for addEveryJob()
        """
        logger.debug("Scheduler.every(): kwargs=%s" % repr(kwargs))

        def decorated(func):
            """ We don't wrap the decorated function!
            """
            self._register(Scheduler.TYPE_EVERY, func, kwargs)

            return func

        return decorated

    def addEvery(self, func, **kwargs):
        """ Add a job which has to be called 'every xxx'

        @param func: job to register
        @type func: callable

        @param kwargs: additional arguments for APScheduler
        @type kwargs: dict
        """
        logger.debug("Scheduler.addEveryJob(): func=%s" % repr(func))
        self._apscheduler.add_interval_job(func, **kwargs)

    def at(self, **kwargs):
        """ Decorator for addAtJob()
        """
        logger.debug("Scheduler.at(): kwargs=%s" % repr(kwargs))

        def decorated(func):
            """ We don't wrap the decorated function!
            """
            self._register(Scheduler.TYPE_AT, func, kwargs)

            return func

        return decorated

    def addAt(self, func, **kwargs):
        """ Add a job which has to be called 'at xxx'

        @param func: job to register
        @type func: callable
        """
        logger.debug("Scheduler.addAtJob(): func=%s" % repr(func))
        self._apscheduler.add_date_job(func, **kwargs)

    def cron(self, **kwargs):
        """ Decorator for addCronJob()
        """
        logger.debug("Scheduler.cron(): kwargs=%s" % repr(kwargs))

        def decorated(func):
            """ We don't wrap the decorated function!
            """
            self._register(Scheduler.TYPE_CRON, func, kwargs)

            return func

        return decorated

    def addCron(self, func, **kwargs):
        """ Add a job which has to be called with cron

        @param func: job to register
        @type func: callable
        """
        logger.debug("Scheduler.addCronJob(): func=%s" % repr(func))
        self._apscheduler.add_cron_job(func, **kwargs)

    def doRegisterJobs(self, obj):
        """ Really register jobs in APScheduler

        @param obj: instance for which a method may have been pre-registered
        @type obj: object
        """
        logger.debug("Scheduler.doRegisterJobs(): obj=%s" % repr(obj))

        for name,func in vars(type(obj)).items():
            method = None
            for trigger,kwargs in getattr(func,'_Sched',()):
                if method is None:
                    method = getattr(obj,name)
                    logger.debug("Scheduler.doRegisterJobs(): %s: func=%s, kwargs=%s" % (trigger, func_name(func), repr(kwargs)))
                    self._apscheduler.add_job(method, trigger=trigger, **kwargs)

    def printJobs(self):
        """ Print pending jobs

        Simple proxy to APScheduler.print_jobs() method.
        """
        self._apscheduler.print_jobs()

    def start(self):
        """ Start the scheduler

        Simple proxy to APScheduler.start() method.
        """
        logger.trace("Scheduler.start()")

        if self._apscheduler is None:
            self._apscheduler = self._type()
            self._apscheduler.add_listener(self._listener, mask=(EVENT_JOB_ERROR|EVENT_JOB_MISSED))

        if not self._apscheduler.running:
            self._apscheduler.start()

            logger.trace("Scheduler.start(): running")

    def stop(self):
        """ Shutdown the scheduler

        Simple proxy to APScheduler.stop() method.
        """
        logger.trace("Scheduler.stop()")

        if self._apscheduler is not None and self._apscheduler.running:
            self._apscheduler.shutdown()

            logger.trace("Scheduler.stop(): stopped")

        self._apscheduler = None

