=========================
The MoaT Version of pknyx
=========================

Author: Matthias Urlichs <matthias@urlichs.de>

Rationale
=========

When I started looking at pknyx, some issues were apparent that motivated
me to radically rewrite some aspects of pknyx.

Using more than one device
--------------------------

Running an entirely separate KNX protocol stack per device does not make
sense. That does not scale. – assume that you want to monitor a building
with 1000 devices. That will open 2000 sockets and create 5000 OS-level
threads.

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

Hop count
+++++++++

Experience shows that the KNX protocol's strange idea to have a hop count
of 7 that's never decremented is a bad idea. pnkyx always decrements the
hop counter.

API Changes in the MoaT version 
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
	dev = MyDevice()
	ets.register(dev)
	ets.mainLoop()

The method ``ETS.weave()`` has been removed.

``ETS.printGroat()`` used to require a device argument. This is now
optional; if not used, the returned table will contain all devices.

