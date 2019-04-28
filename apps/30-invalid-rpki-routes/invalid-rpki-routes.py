#!/usr/bin/env python
################################################################
# (c) CarlosM carlos@xt6labs.io
# 
# 2019-04-18
################################################################

import pytricia
import sqlite3
import logging
import fire
import collections
import pysnooper

dbfile = "../../data/netdata-latest.db"
# cc = 'AR'
rir = 'lacnic'
type = 'ipv4'
maxLen = 24

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

    # def getOneValue(self, wsql):
    #     self.cur = self.con.cursor()
    #     self.cur.execute(wsql)
    #     for x in self.cur:
    #         val = x.pop(0)
    #     return val
    # # end getOneValue
# end netdatadb

class counters:
    def __init__(self):
        self.cnt = {}
    # end

    def set(self, wkey, wval):
        self.cnt[wkey] = wval
    # end

    def get(self, wkey):
        return self.cnt.get(wkey, 0)
    # end

    def inc(self, wkey, winc=1):
        self.cnt[wkey] = self.cnt[wkey] + winc
# end counters

# begin assignValidityStatus
# @pysnooper.snoop(depth=2)
def assignValidityStatus(wroas_trie, wpfx):
    vs = "unknown"
    
    roas = wroas_trie.get(wpfx['prefix'], None)
    if roas == None:
        return vs

    for roa in roas:
        if roa['origin_as2'] == wpfx['origin_as']:
            vs = "valid"
            break
        else:
            vs = "invalid"

    return vs
# end assignValidityStatus

if __name__ == "__main__":
    logging.basicConfig( level=logging.INFO )
    stats = counters()
    logging.debug("Finding RPKI invalid routes - 20190418")

    #
    ndb = netdatadb(dbfile)

    # load roadata into pytricia
    logging.info("Loading ROAs into pytricia")
    roadata_pyt = pytricia.PyTricia(48)
    sql_roas = "SELECT * FROM roadata WHERE ta LIKE '%lacnic%' AND type='{}' " \
        .format(type)
    stats.set('nroas', 0)
    for e in ndb.runsql(sql_roas):
        pfx = str(e['prefix'])
        logging.debug("loading ROA for {} origin {}".format(pfx, e['origin_as']))
        if roadata_pyt.get(pfx, None) == None:
            roadata_pyt[pfx] = [e]
        else:
            roadata_pyt[pfx].append(e)
        stats.inc('nroas')
    #
    logging.info("Loaded {} ROAS into trie".format(stats.get('nroas')) )

    # read routes and look for covering roas, logi assumes that most if not all ROAs will
    # protect _more specific_ prefixes than the ones listed in roas

    stats.set('ninvalid', 0)
    stats.set('nvalid', 0)
    stats.set('nunknown', 0)
    stats.set('nroutes', 0)
    for x in ndb.runsql("SELECT * FROM riswhois WHERE type='{}' AND pfxlen <={} ".format(type, maxLen)):
        stats.inc('nroutes')
        rpfx = str(x['prefix'])
        rov_status = assignValidityStatus(roadata_pyt, x)

        if rov_status == "valid":
                # logging.debug("prefix {} has ROV status VALID, rt_as={}, roa_as={}, roa_pfx={}" \
                #     .format( rpfx, x['origin_as'], roa['origin_as2'], roa['prefix'] ) )
                stats.inc('nvalid')
        elif rov_status == "invalid":
                # logging.info("prefix {} has ROV status INVALID, rt_as={}, roa_as={}, roa_pfx={}" \
                #     .format( rpfx, x['origin_as'], roa['origin_as2'], roa['prefix'] ) )
                stats.inc('ninvalid')
        elif rov_status == "unknown":
            stats.inc('nunknown')


    logging.info("Found {} TOTAL routes".format(stats.get('nroutes')) )
    logging.info("Found {} valid routes".format(stats.get('nvalid')) )
    logging.info("Found {} invalid routes".format(stats.get('ninvalid')) )
    logging.info("Found {} unknown routes".format(stats.get('nunknown')) )
# end script
