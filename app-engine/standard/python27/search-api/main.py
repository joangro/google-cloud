from flask import Flask, request, render_template

from google.appengine.api import search
from google.appengine.api import taskqueue
from google.appengine.api import urlfetch

import os

app=Flask(__name__)

_TASKS_TO_CREATE=2
_TASKS_TO_CREATE_BATCH=2

@app.route('/')
def index():
    data = {'headers':      request.headers,
            'service_name': os.environ.get('CURRENT_MODULE_ID', '(running locally)'),
            'environment':  os.environ}
    return render_template('index.html', data=data)


@app.route('/gendata')
def generate_data():
    import gen_data
    try:
        gen_data.create_index_and_document()
    except Exception:
        import traceback
        traceback.print_exc()
        return "Quotas reached", 500

    return "Document indexed"


@app.route('/task_gendata')
def task_generate_data():
    
    url = 'https://python27-api-search-dot-grauj-gcp.appspot.com/single_urlfetch'
    
    for i in range(_TASKS_TO_CREATE):
        task = taskqueue.add(
            method='GET',
            url='/gendata',
            target='python27-api-search',
            queue_name='search-api'
        )
        '''
        try:
            rpc = urlfetch.create_rpc(deadline=601)
            urlfetch.make_fetch_call(rpc, url)
        except urlfetch.Error as e:
            import traceback
            traceback.print_exc()
        '''
    return "Created task with name {} on queue {} targeting {}".format(task.name, task.queue_name, task.target)


@app.route('/batch_gendata')
def batch_generate_data():
    import gen_data
    try:
        gen_data.batch_create_index_and_document()
    except Exception as e:
        import traceback
        traceback.print_exc()

        return "Quotas reached", 500

    return "Document indexed"


@app.route('/batch_task_gendata')
def batch_task_generate_data():
    
    url = 'https://python27-api-search-dot-grauj-gcp.appspot.com/batch_urlfetch'
    
    for i in range(_TASKS_TO_CREATE_BATCH):
        task = taskqueue.add(
            method='GET',
            url='/batch_gendata',
            target='python27-api-search',
            queue_name='search-api'
        )
        '''
        try:
            rpc = urlfetch.create_rpc(deadline=601)
            urlfetch.make_fetch_call(rpc, url)
        except urlfetch.Error as e:
            import traceback
            traceback.print_exc()
        '''
    return "Created task with name {} on queue {} targeting {}".format(task.name, task.queue_name, task.target)


@app.route('/single_urlfetch')
def single_urlfetch():

    url = 'https://python27-api-search-dot-grauj-gcp.appspot.com/task_gendata'
    
    try:
        result = urlfetch.fetch(url)
    except urlfetch.Error as e:
        import traceback
        traceback.print_exc()


@app.route('/batch_urlfetch')
def batch_urlfetch():

    url = 'https://python27-api-search-dot-grauj-gcp.appspot.com/batch_task_gendata'
    
    try:
        result = urlfetch.fetch(url)
    except urlfetch.Error as e:
        import traceback
        traceback.print_exc()


@app.route('/add_data')
def add_data():
    pass


@app.route('/task_add_data')
def task_add_data():
    task = taskqueue.add(
        method='GET',
        url='/add_data',
        target='python27-api-search',
        queue_name='search_api'
    )
    return "Created task with name {} on queue {} targeting {}".format(task.name, task.queue_name, task.target)


if __name__ == '__main__':
    app.run('127.0.0.1', port=8080, debug=True)

