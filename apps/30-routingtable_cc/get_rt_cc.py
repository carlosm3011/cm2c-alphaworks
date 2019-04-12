#!/usr/bin/env python
##############
# (c) CarlosM carlos@xt6labs.io
# 
# 2019-04-09
##############

import pytricia
import sqlite3
import logging
import fire
import collections

dbfile = "data/netdata-20190325.db"
cc = 'BR'
type = 'ipv6'

stats = collections.Counter()

class netdatadb:
	def __init__(self, wdb):
		try:
			self.con = sqlite3.connect(wdb)
			self.con.row_factory = sqlite3.Row
		except:
			self.conf = False
			raise
	# end init

	def runsql(self, wsql):
		self.cur = self.con.cursor()
		self.cur.execute(wsql)
		return self.cur
	# end runsql
# end netdatadb

def main(cc, type='ipv6', dbfile='data/netdata-20190325.db', verbose='0'):
	ndb = netdatadb(dbfile) 
	pyt = pytricia.PyTricia(48)

	if verbose == 1:
		logging.basicConfig(filename='rt.log', filemode='w', level=logging.DEBUG)
	elif verbose == 0: 
		logging.basicConfig(level=logging.INFO)
	else:
		logging.basicConfig(level=logging.INFO)

	logging.info("Loading {} resources into PyTricia".format(cc))
	logging.info("Looking for {} routes into PyTricia".format(type))
	sql_cc_pfx = "SELECT * FROM numres WHERE cc='{}' AND type='{}' ". \
					format(cc, type)
	for x in ndb.runsql(sql_cc_pfx):
		pfx = str(x['prefix'])
		logging.debug(pfx)
		pyt[pfx] = cc

	# go over routing table and get VE routes
	stats = collections.Counter({'total': 0, 'ccroutes': 0})
	sql_routes = "SELECT * FROM riswhois WHERE type='{}' ".format(type)
	for x in ndb.runsql(sql_routes):
		rpfx = str(x['prefix'])
		rcc = pyt.get(rpfx, None)
		stats['total'] += 1
		if rcc == cc:
			covering_pfx = pyt.get_key(rpfx)
			logging.info("Found {} route: {}, under allocation {}".format(cc, rpfx, covering_pfx))
			stats['ccroutes'] += 1
		# end if
	# end for

	logging.info("Found {} {} routes for type {}". \
		format(stats['ccroutes'], cc, type))
	logging.info("Total routes: {}".format(stats['total']))
## end main

if __name__ == "__main__":
	fire.Fire(main)
	
# END