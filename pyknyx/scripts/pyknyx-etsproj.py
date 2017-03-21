#!/usr/bin/python3

from __future__ import print_function,absolute_import

# 
# This quick-and-dirty script extracts information from an ETS4/5 project
# file.
#
# Usage:
#
# etsproj FILE.proj
# -- prints a directory, with uncompressed file size
#
# etsproj FILE.proj FILE.xml
# -- extracts and prints that file
#
# etsproj FILE.proj GA
# -- extracts group addresses

# TODO: convert to a "real" library

import zipfile
import sys
import re
import xml.etree.ElementTree as ET
import codecs
import attr

from pyknyx.stack.groupAddress import GroupAddress
from pyknyx.core.dptXlator.dptId import DPTID

ns = {}

DPTs = {}
DPTsz = {}

def proj_init(zf):
#	<DatapointTypes>
#      <DatapointType Id="DPT-1" Number="1" Name="1.xxx" Text="1-bit" SizeInBit="1" PDT="PDT-50">
#        <DatapointSubtypes>
#          <DatapointSubtype Id="DPST-1-1" Number="1" Name="DPT_Switch" Text="switch" Default="true">
#            <Format>
#              <Bit Id="DPST-1-1_F-1" Cleared="Off" Set="On" />
	with zf.open("knx_master.xml") as f:
		pi = ET.parse(f)

	ns = {}
	t = pi.getroot().tag
	pns = t.index('}')
	if pns > 0:
		ns['KNX'] = t[1:pns]

	for a in pi.findall(".//KNX:DatapointType", ns):
		d = DPTID(main=int(a.get("Number")))
		DPTs[a.get("Id")] = d
		sz = a.get("SizeInBit",None)
		if sz is not None:
			sz = int(sz)

		for b in a.findall(".//KNX:DatapointSubtype", ns):
			d = DPTID(main=int(a.get("Number")), sub=int(b.get("Number")))
			DPTs[b.get("Id")] = d
			if sz is not None:
				DPTsz[sz] = d
				sz = None

def proj_id(zf):
	pid = None
	for i in zf.infolist():
		if i.filename.startswith("P-") and i.filename.endswith(".signature") \
				and len(i.filename) == 16:
			if pid is None:
				pid = i.filename[2:6]
			else:
				raise IndexError("dup PID",pid,i.filename[3:7])
	return pid
	
@attr.s
class GroupAddr:
	id = attr.ib()
	ga = attr.ib()
	path = attr.ib()
	dpt = attr.ib(default=None)
GAs = {}
GAcheck = set()

def processConns(zf,pi):
	# processETS4GroupAddressConnections
	if not GAcheck: # nothign to do
		return
	for useObjSize in (False,True):
		for useRecv in (True,False):
			for pe in pi.findall(".//KNX:ComObjectInstanceRef", ns):
				dpt = pe.get("DatapointType", None)
				for _dp in pe.findall("./KNX:Connectors", ns):
					for dp in _dp.findall("./KNX:%s[@GroupAddressRefId]" % ("Receive" if useRecv else "Send", ),  ns):
						gid = dp.get("GroupAddressRefId",None)
						if gid is not None and gid in GAcheck:
							if dpt is None:
								rid = pe.get("RefId")
								dpt = processGroupConns(zf,rid, useObjSize)
								if dpt is None:
									continue
							else:
								dpt = DPTs[dpt]
							GAs[gid].dpt = dpt
							GAcheck.remove(gid)

devices = {}

def processGroupConns(zf,rid, useObjSize):
	pt = rid.split('_',2)
	fn = "%s/%s_%s.xml" % (pt[0],pt[0],pt[1])
	try:
		devs = devices[fn]
	except KeyError:
		with zf.open(fn) as f:
			pi = ET.parse(f)

		ns = {}
		t = pi.getroot().tag
		pns = t.index('}')
		if pns > 0:
			ns['KNX'] = t[1:pns]

		devs = {}
		for d in pi.findall(".//KNX:ComObjectRef", ns):
			devs[d.get("Id")] = d
		for d in pi.findall(".//KNX:ComObject", ns):
			devs[d.get("Id")] = d
		devices[fn] = devs

	dev = devs[rid]
	dpt = processETS4ComObj(dev,useObjSize)
	if dpt is not None:
		return dpt
	dev = devs[dev.get("RefId")]
	dpt = processETS4ComObj(dev,useObjSize)
	return dpt

def processETS4ComObj(dev,useObjSize):
	dpt = dev.get("DatapointType",None)
	if dpt:
		dpt = dpt.split(' ',1)[0]
		return DPTs[dpt]
	if useObjSize:
		sz = dev.get("ObjectSize", None)
		if sz:
			if sz == "1 Bit":
				sz = "DPST-1-1"
			elif sz == "1 Byte":
				sz = "DPST-5-1"
			elif sz == "2 Bytes":
				sz = "DPST-9-1"
			else:
				sz = sz.split(" ",1)
				if sz[1].startswith("byte"):
					sz = int(sz[0]) * 8
				else:
					sz = int(sz[0])
				sz = DPTsz[sz].id
			return DPTs[sz]
	return None

def proj_sub_ga(ga,*s):
	for f in ga.iterfind("./KNX:GroupRange", ns):
		yield from proj_sub_ga(f,*(s+(f.get("Name"),)))
		# <GroupRange Id="P-02DA-0_GR-4" Name="Sonstiges" RangeStart="4096" RangeEnd="6143">
		# <GroupAddress Id="P-02DA-0_GA-78" Address="2640" Name="DL Keller" />
	for f in ga.iterfind("./KNX:GroupAddress", ns):
		dpt = f.get("DatapointType",None)
		gid = f.get("Id")
		if not dpt: # None or ''
			GAcheck.add(gid)
		yield GroupAddr(id=gid, ga=GroupAddress(int(f.get("Address"))).address, path=s+(f.get("Name"),), dpt=dpt)

def proj_et(zf,pid):
	try:
		f = zf.open("P-%s/Project.xml" % (pid,))
	except KeyError:
		f = zf.open("P-%s/project.xml" % (pid,))
	try:
		pi = ET.parse(f)
		pns = pi.getroot().tag.index('}')
		if pns > 0:
			ns['KNX'] = pi.getroot().tag[1:pns]
	finally:
		f.close()
        #   <Project Id="P-02DA">
        #      <ProjectInformation Name="Urlichs" LastModified="2015-08-14T07:06:12" ProjectStart="2015-06-26T09:33:35" ProjectId="0" ProjectTracingLevel="None" Hide16BitGroupsFromLegacyPlugins="1" GroupAddressStyle="ThreeLevel" CompletionStatus="Undefined" />

		pnr = pi.find(".//KNX:Project[@Id='P-%s']/KNX:ProjectInformation" % (pid,), ns).get("ProjectId")
	with zf.open("P-%s/%s.xml" % (pid,pnr)) as f:
		pi = ET.parse(f)
	for ga1 in pi.findall(".//KNX:GroupAddresses/KNX:GroupRanges", ns):
		for ga in proj_sub_ga(ga1):
			GAs[ga.id] = ga
	processConns(zf,pi)
	for ga in GAs.values():
		print(ga)

def print_ga(zf):
	proj_init(zf)
	pid = proj_id(zf)
	proj_et(zf,pid)
	for x in GAs.values():
		print(x)

	

def main(args=None):
	if args is None:
		args = sys.argv[1:]
	if not args:
		print("Usage: %s file.etsproj [GA | filename]" % (sys.argv[0],), file=sys.stderr)
		return
	

	with zipfile.ZipFile(args[0]) as zf:
		if len(args) == 1:
			for i in zf.infolist():
				print(i.file_size, i.filename)
		elif len(args) == 2 and args[1] == "GA":
			print_ga(zf)
			
		elif len(args) == 2:
			with zf.open(args[1]) as f:
				utf = codecs.getincrementaldecoder("utf-8")()
				while True:
					b = f.read(4096)
					if not b:
						return
					sys.stdout.write(utf.decode(b,False))
				sys.stdout.write(utf.decode(b'',True))

if __name__ == "__main__":
	main()
