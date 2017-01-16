########################################################
# RDAP In-memory Cache using REDIS
########################################################

import rdap
import redis
import time

class RDAPCache(object):
    def __init__(self):
        self.mcc = redis.Redis(host="redis")
        pass
    # end init
        
    def get_and_cache(self, w_pfx):
        if w_pfx:
            self.mcc.incr("queries",1)
            rdap_ans = self.mcc.get(w_pfx)
            if rdap_ans:
                self.mcc.incr("hits",1)
                return rdap_ans
            else:
                # return "IP address is %s" % (ipaddr)
                self.mcc.incr("misses",1)
                rdap_ans = rdap.rdap_client("https://rdap.lacnic.net/rdap/ip/%s" % w_pfx)
                if rdap_ans != "RDAP ERROR":
                    self.mcc.set(w_pfx, rdap_ans)
                return rdap_ans
        else:
            return False
        
    # end def 
# end class

if __name__ == "__main__":
    print "rdap in memory cache"
