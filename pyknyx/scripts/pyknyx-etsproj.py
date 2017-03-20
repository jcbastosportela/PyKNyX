#!/usr/bin/python3

from __future__ import print_function,absolute_import

import zipfile
import sys
import re
import xml.etree.ElementTree as ET
import codecs

from pyknyx.stack.groupAddress import GroupAddress

ns = {}

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
	
def proj_sub_ga(ga,*s):
	for f in ga.iterfind("./KNX:GroupRange", ns):
		yield from proj_sub_ga(f,*(s+(f.get("Name"),)))
		# <GroupRange Id="P-02DA-0_GR-4" Name="Sonstiges" RangeStart="4096" RangeEnd="6143">
		# <GroupAddress Id="P-02DA-0_GA-78" Address="2640" Name="DL Keller" />
	for f in ga.iterfind("./KNX:GroupAddress", ns):
		yield GroupAddress(int(f.get("Address"))).address,s+(f.get("Name"),)

def proj_et(zf,pid):
	with zf.open("P-%s/Project.xml" % (pid,)) as f:
		pi = ET.parse(f)
		pns = pi._root.tag.index('}')
		if pns > 0:
			ns['KNX'] = pi._root.tag[1:pns]
        #   <Project Id="P-02DA">
        #      <ProjectInformation Name="Urlichs" LastModified="2015-08-14T07:06:12" ProjectStart="2015-06-26T09:33:35" ProjectId="0" ProjectTracingLevel="None" Hide16BitGroupsFromLegacyPlugins="1" GroupAddressStyle="ThreeLevel" CompletionStatus="Undefined" />

		pnr = pi.find(".//KNX:Project[@Id='P-%s']/KNX:ProjectInformation" % (pid,), ns).get("ProjectId")
	with zf.open("P-%s/%s.xml" % (pid,pnr)) as f:
		pi = ET.parse(f)
		for ga1 in pi.findall(".//KNX:GroupAddresses/KNX:GroupRanges", ns):
			yield from proj_sub_ga(ga1)

	

def print_ga(zf):
	pid = proj_id(zf)
	pt = proj_et(zf,pid)
	for x in pt:
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
