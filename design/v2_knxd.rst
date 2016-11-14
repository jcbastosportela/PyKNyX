================================
pknxd: The knxd Version of pknyx
================================

Author: Matthias Urlichs <matthias@urlichs.de>

Rationale
=========

The KNX router I maintain (`knxd`_) is written in somewhat-dated C++ which
requires a non-standard library. When I discovered `pKNyX`_, I saw that it
might eventually replace `knxd`_. So I decided to get started.

In addition, some aspects of `pKNyX`_ didn't work for me and shouted
"Rewrite me!". I couldn't ignore that temptation.

_knxd: https://github.com/knxd/knxd
_pKNyX: http://www.pknyx.org/

Changes to pKNyX
================

The following sub-chapters describe the changes I implemented.

Using more than one device
--------------------------

Running an entirely separate KNX protocol stack per device does not make
sense. That does not scale.

Aassume that you want to monitor a building with 1000 devices. That will
open 2000 sockets and create 5000 OS-level threads, half of which will wake
up for each packet, only to decide that it's not for them.

Thus, the "master" object in pknyx is no longer a device, but the ETS object.
This is no longer a singleton, allowing you to run more than one ETS stack
in a single program (if desired). ETS will forward incoming packets to all
devices. TODO: propagate group membership to ETS, in order to reduce
overhead.

Using more than one transport
-----------------------------

It may make sense to use more than one transport. For instance, if you have
two KNX interfaces which don't speak multicast, you either need to run a
separate KNX daemon – or you teach pknyx to support more than one
transport.

Also, it may make sense for different pknys devices to talk to each other,
e.g. for testing, without transmitting multicast messages.

For this reason, there no longer is a notion of a "Transport" in pknyx.
Instead, the Layer-2 drivers are classified by whether they support more than
one device (= physical address). The ETS class contains a dispatcher which
simply copies each packet to all other interfaces which want it. Of course
it decrements the hop count when forwarding from one bus to another.

This means that the meanings of data "indication" and "request", as used by
the OSI layering, seem reversed. A Request is now something that is
destined for the ETS object while an Indication is a data packet that has
been distributed by ETS: from the point-of-view of pKNyX, the ETS object is
the lowest layer.

Assigning physical addresses
----------------------------

Usually you don't really care about a device's physical address, as long as
it is routed correctly and it isn't used by anything else on the bus. 

Thus, ETS will assign device addresses dynamically. At init time you can
specify how many free addresses there are. If your program registers more
devices than that, an error is triggered.

The default is to share the ETS object's address with the first device gets
registered. This obviously only works when you only have one device.

Split off tests
---------------

Originally, tests were based on unittest and included in the main code.
You tested a module by simply running it.

I decided to move all tests into a "tests" directory.

* Use `pytest` instead of unittest (much nicer)
* Ability to test installed or other versions of pKNyX
* More easily runnable by ``setup.py``

Minor fixes
-----------

* Python 3 support
* merged GrOAT listings
* added integration tests
* multicast socket

Hop count
+++++++++

Experience shows that the KNX protocol's strange idea to have a hop count
of 7 that's never decremented is a bad idea. pnkyx always decrements the
hop counter.

API Changes in the knxd version 
===============================

ETS
+++

The address and low-level driver arguments of class Device have been moved
to the ETS object. Also, ETS object is no longer a singleton. Thus, this code

	dev = MyDevice("1.2.3")
	ETS().register(dev)
	ETS().weave(dev) # aliases: bind(), link()
	dev.mainLoop()

needs to be replaced with

	ets = ETS("1.2.3")
	dev = MyDevice(ets)
	ets.mainLoop()

The method ``ETS.weave()`` has been removed.

``ETS.printGroat()`` used to require a device argument. This is now
optional; if not used, the returned table will contain all devices.

Planned changes ("TODO")
========================

* more tests, esp. end-to-end of the example code snippets

* Requiring a separate class per device isn't very Python-ish

* … and doesn't lend itself to generating multiple devices from a config file

* more code cleanups

* declare datapoints etc. as objects, not dicts

* propagate group address filtering down the stack

* (adding a dispatch table instead of looping through all the data layers)

* route datagrams to, and add caching of, individual addresses

* add using a socket to knxd or a tunnel

* possibly port more features of knxd

* possibly² add code for handling large knx networks, e.g. group address filtering and translation

