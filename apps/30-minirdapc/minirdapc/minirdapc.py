#!/usr/bin/env python3.7
#----------------------------------------------------------------------------------
# minirdapc
#
# (c) carlos@xt6.us
# 
# Changed: 2019-03-14
#----------------------------------------------------------------------------------

import click
import requests
import shelve
import datetime
import time
import pyjq
import json

class rdap_client:

    # Default constructor
    def __init__(self, w_base_url, w_cache_file='var/rdap_cache.db'):
        self.base_url = w_base_url
        self.rdap_cache = shelve.open(w_cache_file)
        self.max_cache_time = 60
        self.last_response = None
    # end default constructor

    # destructor
    def __del__(self):
        self.rdap_cache.close()
    # end

    # http_get
    def rdap_http_get(self, w_uri):
        try:
            rdap_url = self.base_url + w_uri
            print(rdap_url)
            r = requests.get(rdap_url)
            if r.status_code == 200:
                return r.json()
            else:
                return "{'status code': '%s', 'response': %s}" % (str(r.status_code), repr(r) )
        except:
            raise
    # end http_get

    # pyjq interface
    def _pyjq(self, w_query, w_json = None):
        """
        Runs a jq query against a json structure
        """

        if w_json == None:
            q_json = self.last_response
        else:
            q_json = w_json

        try:
            r = pyjq.first(w_query, q_json)
        except:
            raise
        #
        return r
    # end pyjq

    # get_poc ##############################################################################################
    def get_poc(self, w_role, w_depth=0, w_json = None):
        """
        get_poc() retrieves the handles for different roles (abuse, technical, registrant). Can be used
        in 'simple' or 'deep' mode. In simple mode only the handle is returned, in deep mode an additional
        RDAP query is made and detailed contact information is returned.
        """
        if w_json == None:
            q_json = self.last_response
        else:
            q_json = w_json
        #
        if w_role not in ['abuse', 'technical', 'registrant']:
            raise ValueError("Unknown POC role")
        #
        # jq = '.entities[] | select (.roles[0] == "{}") | .handle + " , " + .roles[0]'.format(w_role)
        jq = '.entities[] | select (.roles[0] == "{}") | .handle'.format(w_role)
        # print("jq string={}".format(jq))
        r = self._pyjq(jq)
        #
        if w_depth == 0:
            return r
        elif w_depth == 1:
            # further query rdap to get email addresses
            r2 = self.rdap_query("entity", r)
            email = self._pyjq('.vcardArray[1] | .[]  | select ( .[0] == "email") | .[3]', r2)
            jr = {'handle': r, 'email': email}
            return jr
    # end get_poc ##########################################################################################

    # rdap query ###########################################################################################
    def rdap_query(self, w_type, w_query):

        if w_type not in ['ip', 'autnum', 'entity']:
            raise ValueError("Wrong query type")

        try:
            rdap_uri = "/"+w_type+"/"+w_query
            # first check if answer is available in local cache and fresh enough
            cached_r = self.rdap_cache.get(rdap_uri, { 'json': None, 'timestamp': 0, 'hits': 0})
            if cached_r['json'] == None or (cached_r['timestamp'] - time.time()) > self.max_cache_time:
                # if not, do an http query
                r = self.rdap_http_get(rdap_uri)
                # TODO: No guardar en el cache cosas que no sirven!!
                # store result in cache
                cached_r = { 'json': r, 'timestamp': int(time.time()), 'hits': 0}
                self.rdap_cache[rdap_uri] = cached_r
            else: 
                # return the result available in cache
                r = cached_r['json']
                pass
        except:
            r = False
            raise
        self.last_response = r
        return r
    # end rdap query #######################################################################################

# end class rdap_client

# cli #######################################################################################
@click.command()
@click.option("--query", help="String to query RDAP for.")
@click.option("--type", "rdap_type", help="RDAP query type, one of autnum, ip or entity")
@click.option("--host", default="https://rdap.lacnic.net/rdap", help="RDAP server to query. Optional, defaults to LACNIC")
def cli(query, rdap_type, host):
        rdapc = rdap_client(host)
        res = rdapc.rdap_query(rdap_type, query)
        print( json.dumps(res, indent=3, sort_keys=True) )
        # print (str(res))
## end cli ##################################################################################

if __name__ == "__main__":
    cli()

#--END-----------------------------------------------------------------------------