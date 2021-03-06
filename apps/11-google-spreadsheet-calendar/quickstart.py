#!/usr/bin/env python2.7
"""
Shows basic usage of the Sheets API. Prints values from a Google Spreadsheet.
"""
from __future__ import print_function
from apiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools

# Setup the Sheets API
SCOPES = 'https://www.googleapis.com/auth/spreadsheets.readonly'
store = file.Storage('credentials.json')
creds = store.get()
if not creds or creds.invalid:
    flow = client.flow_from_clientsecrets('client_secret_1.json', SCOPES)
    creds = tools.run_flow(flow, store)
service = build('sheets', 'v4', http=creds.authorize(Http()))

# Call the Sheets API
# SPREADSHEET_ID = '1BxiMVs0XRA5nFMdKvBdBZjgmUUqptlbs74OgvE2upms'
SPREADSHEET_ID = '144KwlsKQBQj9PBeAmE8x8dOuEY-Sl6cEZvIgI40hSc8'
RANGE_NAME = 'Detalle agenda!A1:F10'
result = service.spreadsheets().values().get(spreadsheetId=SPREADSHEET_ID,
                                             range=RANGE_NAME).execute()
values = result.get('values', [])
if not values:
    print('No data found.')
else:
    print('Time, Descr, Room:')
    for row in values:
        # Print columns A and E, which correspond to indices 0 and 4.
	try:
        	print('%s, %s, %s' % (row[0], row[1], row[5]))
	except:
		print(row)
	# print(row)
	# for v in row:
	# 	print("---> %s" % v)
	# print(" ")
