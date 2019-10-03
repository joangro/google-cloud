from flask import Flask, request, render_template
from google.appengine.api import runtime

import os

app=Flask(__name__)

@app.route('/')
def index():
    data = {'headers':      request.headers,
            'service_name': os.environ.get('CURRENT_MODULE_ID', '(running locally)'),
            'environment':  os.environ}
    return render_template('index.html', data=data)

@app.route('/runtime')
def runtime_stats():
    mem = {}
    
    mem_use = runtime.memory_usage()
    
    mem['Memory (current)'] = mem_use.current()
    mem['Memory (average 1m)'] = mem_use.average1m()
    mem['Memory (average 10m)'] = mem_use.average10m()

    cpu = {}

    cpu_use = runtime.cpu_usage()
    cpu['CPU (Total)'] = cpu_use.total()
    cpu['CPU (Average 1m)'] = cpu_use.rate1m()
    cpu['CPU (Average 10m)'] = cpu_use.rate10m()
    
    return render_template('runtime.html', cpu=cpu, mem=mem)

if __name__ == '__main__':
    app.run('127.0.0.1', port=8080, debug=True)
