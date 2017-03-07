import urllib2
import simplejson

def rdap_client(w_query):
    try:
        rsp = urllib2.urlopen(w_query)
        json = rsp.read()
        return json
    except:
        return "RDAP ERROR"
