#!/usr/bin/python
import keen
import sys
import subprocess
import string

keen.project_id = "56eae5a3d2eaaa4d7181e9de"
keen.write_key = "3ce6df1a63b8aa1fbb9c7a929f192e93e8ea5d4fad19fa75c026b4d32b5ff22a53fb6bd3f9fa5ccb81abfae65edb6735fa1f6615a5863666c7ae14aa75a9740d3d8ab7a183a720d720d6fb0121b67ffea11974107a018dd02c03b1c19d5bf6ab"
keen.read_key = "05fdaa87631ae5b783cd24c516e9acfcecdc50e1f20a7c77928a378962dc05d1c9ac90a6f9394dc93298b14128fe7429b32cb7faa9b625ba6e617ca1f4ddf2bf9bda86ea4ce5e78d6fae3870a1b1fdc6821cea2f9cce4594bd5a816279100527"
keen.master_key = "F361F6CC3751F727226F0E371CA39A0376AAA6B212DF709E501F0FA8A91041BE"

# get parameters, use field_name field_value ...

evp = []

for x in xrange(1,len(sys.argv)-1,2):
	evp.append({"field_name": sys.argv[x], "field_value": sys.argv[x+1]})


# build and send event
hname = string.rstrip(subprocess.check_output(["hostname"]))
evt= {
  "category": "server monitoring",
  "server_name": hname,
}

for y in xrange(0,len(evp)):
	evt[evp[y]["field_name"]]= float(evp[y]["field_value"])

r = None
print "sending event %s " % (evt)
r = keen.add_event("server_monitoring", evt)

if r != None:
	print "Non-null return value: %s" % (r)
else:
	print "Probable success!"
