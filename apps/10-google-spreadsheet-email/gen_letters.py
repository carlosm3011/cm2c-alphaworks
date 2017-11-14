#!/opt/local/bin/python2.7
######
# gen letters
######

import smtplib
from email.mime.text import MIMEText
import sys
import string
import csv
import json
import gspread
from oauth2client.client import SignedJwtAssertionCredentials

## begin gen_letter
def gen_letter(row, template):
	f = open(template, "r")
	template_text = string.Template(f.read())
	final_text = template_text.substitute(row)
	final_text_filename = "tmp/%s.txt" % row["NAME"]
	final_text_filename = final_text_filename.replace(" ","_").lower()
	g = open(final_text_filename, "w")
	g.write(final_text)
	f.close()
	g.close()
	return final_text_filename
## end gen_letter

## begin send_email
def send_email(text_fn, row):
	# Open a plain text file for reading.  For this example, assume that
	# the text file contains only ASCII characters.
	fp = open(text_fn, 'rb')
	# Create a text/plain message
	email_text = fp.read()
	msg = MIMEText(email_text, 'plain', 'UTF-8')
	fp.close()
	# fill fields
	me = "Carlos Martinez <carlos@lacnic.net>"
	you = row["EMAIL"]
	msg["Subject"] = "Codigo para registro gratuito al IETF95 - LACNIC"
	msg["From"] = me
	msg["To"] = you
	msg['Content-Type'] = "text/plain; charset=utf-8"
	msg['Content-Transfer-Encoding'] = "quoted-printable"
	msg['Disposition-Notification-To'] = me
	msg['Return-Receipt-To'] = me
	# instantiate smtp server
	try:
		svr = smtplib.SMTP("mail.lacnic.net.uy")
		svr.sendmail(me, [you], msg.as_string())
		return True
	except:
		raise
		return False
## end send_email

## begin MAIN
try:
	invitees_file = sys.argv[1]
	letter_template = sys.argv[2]
except:
	print "usage: ./gen_letters.py 'spreadsheet name' letter_template"
	sys.exit(1)

json_key = json.load(open('ietf-letters-176a43ddd503.json'))
scope = ['https://spreadsheets.google.com/feeds']
credentials = SignedJwtAssertionCredentials(json_key['client_email'], json_key['private_key'], scope)

gclient = gspread.authorize(credentials)
gspread = gclient.open(invitees_file)
gwsheet = gspread.sheet1

print "reading invitees from %s" % (invitees_file)

# generate letters
for irow in gwsheet.get_all_records():
	# print row
	print "generating invitation letter for %s (%s) with code %s" % (irow["NAME"], irow["EMAIL"], irow["CODE"])
	ftfn = gen_letter(irow, letter_template )
	if irow["SEND"] == 1:
		print "\tsending email to %s" % (irow["EMAIL"]),
		r = send_email(ftfn, irow)
		if r:
			print "success!"
		else:
			print "FAILED!"
	else:
		print "\tnot sending email"

## END MAIN ###############################################################################

## END FILE ###############################################################################
