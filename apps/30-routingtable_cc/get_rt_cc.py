##############
#
#
##############

import pytricia
import sqlite3
import logging

dbfile = "data/netdata-20190325.db"
cc = 'BR'
type = 'ipv6'

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

if __name__ == "__main__":
	ndb = netdatadb(dbfile)
	pyt = pytricia.PyTricia(48)

	logging.basicConfig(level=logging.INFO)

	logging.info("Loading {} resources into PyTricia".format(cc))
	sql_cc_pfx = "SELECT * FROM numres WHERE cc='{}' AND type='{}' ". \
					format(cc, type)
	for x in ndb.runsql(sql_cc_pfx):
		pfx = str(x['prefix'])
		logging.debug(pfx)
		pyt[pfx] = cc

	# go over routing table and get VE routes
	cnt_routes = 0
	tot_routes = 0
	sql_routes = "SELECT * FROM riswhois WHERE type='{}' ".format(type)
	for x in ndb.runsql(sql_routes):
		rpfx = str(x['prefix'])
		rcc = pyt.get(rpfx, None)
		tot_routes = tot_routes + 1
		if rcc == cc:
			logging.info("Found {} route: {}".format(cc, rpfx))
			cnt_routes = cnt_routes + 1
		# end if
	# end for

	logging.info("Found {} {} routes".format(cnt_routes, cc))
	logging.info("Total routes: {}".format(tot_routes))

# END