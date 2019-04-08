####################################################
# RDAP in-memory temp storage front end
# (c) carlos@xt6.us
####################################################


from flask import Flask
from flask import render_template
# from pymemcache.client.base import Client
import redis
# from rdap import rdap_client
from rdapcache import RDAPCache
import time

app = Flask(__name__)
# mcc = Client(("memcached", 11211))
mcc = redis.Redis(host="redis")
rc = RDAPCache()
start_time = time.time()

@app.route('/')
def hello():
    # count = redis.incr('hits')
    count = mcc.get("count")
    if not count:
        count = 0
        mcc.set("count", count)
    else:
        mcc.set("count", int(count)+1)
    return '<h1>Hello World! I have been seen {} times.\n</h1>'.format(count)

@app.route('/rdap')
def route_rdap():
    abort(503)

@app.route('/stats')
def route_stats():
    stats = {'queries': mcc.get("queries"),
             'hits': mcc.get("hits"),
             'misses': mcc.get("misses"),
             "uptime": time.time()-start_time}
    return render_template("stats.html", stats=stats)

@app.route('/rdap/ip/<path:pfx>')
def route_rdap_ip(pfx):
    if pfx:
        t0 = time.time()
        rdap_ans = rc.get_and_cache(pfx)
        rsp = {"json": rdap_ans.decode('ascii', 'ignore'), "time": time.time()-t0}
        return render_template("response.html", rsp=rsp)
    else:
        abort(401)

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True, threaded=True)
