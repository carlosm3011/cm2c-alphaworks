######
# Create ICS Agenda for LACNIC 27
# (c) Carlos M. Martinez, carlos@lacnic.net
######

import sys
import string
import csv
import json
import gspread
import codecs
import unicodedata
from oauth2client.client import SignedJwtAssertionCredentials
from ics import Calendar,Event
from unidecode import unidecode

# parameters #######
agenda_gsheet_name = "Propuesta Agenda LACNIC 27.xlsx"
# end parameters ###

json_key = json.load(open('lacnic-ics-agenda-8d9f8acc9f7b.json'))
scope = ['https://spreadsheets.google.com/feeds']
credentials = SignedJwtAssertionCredentials(json_key['client_email'], json_key['private_key'], scope)

gclient = gspread.authorize(credentials)
gspread = gclient.open(agenda_gsheet_name)
gwsheet = gspread.get_worksheet(1)

# generate Calendar
cal = Calendar()
for grow in gwsheet.get_all_records():
	if grow["ICSDate"]!="":
		try:
			# print "%s | %s | %s " % (grow["DESC"], grow["ICSDate"], grow["ICSTime"])
			evt = Event()
			# evt.name = unicodedata.normalize('NFKD', unicode(grow["DESC"]))
			# evt.name = "Nombre evento"
			# evt.name = grow["DESC"].encode('ascii', 'replace')
			# evt.name = grow["DESC"]
			evt.name = unidecode(grow['DESC'])
			(t_begin, t_end) = grow["ICSTime"].split("-")
			d_begin = "%sT%s:00-0300" % (grow["ICSDate"], t_begin.strip())
			evt.begin = d_begin.replace(":","").replace(".","")
			d_end = "%sT%s:00-0300" % (grow["ICSDate"], t_end.strip())
			evt.end = d_end.replace(":","").replace(".","")
			cal.events.append(evt)
			print "Added %s starting %s ending %s" % (evt.name, d_begin, d_end)
			# print "Added %s, event %s" % (grow['DESC'],evt)
		except:
			print grow
			raise
# END for grow

# Write ics file to disk
with codecs.open("lacnic27.ics", "w", encoding="utf-8") as fn:
	fn.writelines(cal)

## END MAIN ###############################################################################

## END FILE ###############################################################################
