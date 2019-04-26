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

dbfile = "../../data/netdata-latest.db"
cc = 'AR'
rir = 'lacnic'
type = 'ipv4'

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
def assignValidityStatus(wroas, wpfx):
    vs = "valid"
    
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
    for x in ndb.runsql("SELECT * FROM riswhois WHERE type='{}' AND pfxlen <=24 ".format(type)):
        rpfx = str(x['prefix'])
        roas = roadata_pyt.get(rpfx, None)
        if roas == None:
            logging.debug("prefix {} has ROV status NOT_FOUND".format( rpfx ))
        else:
            rov_status = assignValidityStatus(roas, rpfx)

            if rov_status == "valid":
                    # logging.debug("prefix {} has ROV status VALID, rt_as={}, roa_as={}, roa_pfx={}" \
                    #     .format( rpfx, x['origin_as'], roa['origin_as2'], roa['prefix'] ) )
                    stats.inc('nvalid')
            elif rov_status == "invalid":
                    # logging.info("prefix {} has ROV status INVALID, rt_as={}, roa_as={}, roa_pfx={}" \
                    #     .format( rpfx, x['origin_as'], roa['origin_as2'], roa['prefix'] ) )
                    stats.inc('ninvalid')


            # for roa in roas:
            #     # print(roa)
            #     logging.debug("prefix {} has covering ROA ({}, {})" \
            #         .format( rpfx, roa['prefix'], roa['origin_as2'] ))
            #     if roa['origin_as2'] == x['origin_as']: 
            #         logging.debug("prefix {} has ROV status VALID, rt_as={}, roa_as={}, roa_pfx={}" \
            #             .format( rpfx, x['origin_as'], roa['origin_as2'], roa['prefix'] ) )
            #         stats.inc('nvalid')
            #     else:
            #         logging.info("prefix {} has ROV status INVALID, rt_as={}, roa_as={}, roa_pfx={}" \
            #             .format( rpfx, x['origin_as'], roa['origin_as2'], roa['prefix'] ) )
            #         stats.inc('ninvalid')

    logging.info("Found {} valid routes".format(stats.get('nvalid')) )
    logging.info("Found {} invalid routes".format(stats.get('ninvalid')) )
# end script
