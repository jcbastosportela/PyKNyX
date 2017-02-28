This is PyKNyX (pronounced somewhat like "picnic",
mainly because implementing KNX stuff is not one).


Overview
========

PyKNyX is a KNX stack written in Python. It supports virtual devices and
multiple bus interfaces.

Current status: the only interface that's actually in the code is the
standard KNX multicast. If you want to talk to anything else, run "knxd"
(on the same computer is fine). You'll need either the "-b ip:" or
the "-R -S" options.

PyKNyX is a fork of pKNyX. It is not API-compatible.

Future plans
============

Support packets to a device's physical address.

Drop threads in favor of asyncio (Python 3 only).

Possibly extend PyKNyX to serve as a replacement for knxd.

Changes
=======

PyKNyX 1.0
----------

The main loop has been moved to the ETS object, which is no longer a
singleton. It is also now responsible for assigning physical addresses to
drivers. This allows you to create more than one device per ETS instance,
as well as more than one driver to actually talk to a bus. You can also run
more than one ETS instance within a process.

FunctionalBlock and Device setup has been rewritten. Devices can now be set
up by passing its physical address and the group address linkage to the
object's constructor; it is no loger required to create a new class for
each object.

History
=======

PyKNyX is a fork of pKNyX. Its author requested a name change.

The original documentation for pKNyX can be found at http://www.pknyx.org

See the file "doc/rationale.rst" for more rationale and documentation.

