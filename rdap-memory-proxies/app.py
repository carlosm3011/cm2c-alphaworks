####################################################
#
#
####################################################


from flask import Flask
from flask import render_template
from pymemcache.client.base import Client
from rdap import rdap_client
import time

app = Flask(__name__)
mcc = Client(("memcached", 11211))
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
        mcc.add("queries",0)
        mcc.incr("queries",1)
        rdap_ans = mcc.get(pfx)
        if rdap_ans:
            mcc.add("hits",0)
            mcc.incr("hits",1)
            # return rdap_ans
        else:
            # return "IP address is %s" % (ipaddr)
            mcc.add("misses",0)
            mcc.incr("misses",1)
            rdap_ans = rdap_client("https://rdap.lacnic.net/rdap/ip/%s" % pfx)
            if rdap_ans != "RDAP ERROR":
                mcc.set(pfx, rdap_ans)
            # return rdap_ans
        rsp = {"json": rdap_ans.decode('ascii', 'ignore'), "time": time.time()-t0}
        return render_template("response.html", rsp=rsp)
    else:
        abort(401)

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True, threaded=True)
