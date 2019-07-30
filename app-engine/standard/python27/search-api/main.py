from flask import Flask, request, render_template

from google.appengine.api import search
from google.appengine.api import taskqueue
from google.appengine.api import urlfetch

import os, time

app=Flask(__name__)

# Some env vars for the execution of the program. Added them here for visibility, instead of on the app.yaml.
_TASKS_TO_CREATE=2
_TASKS_TO_CREATE_BATCH=2
_LOAD_TEST=True
_TIME_BETWEEN_REQUESTS=3 # (In seconds)


'''
DEFAULT: Handler to display basic app info
'''
@app.route('/')
def index():
    data = {'headers':      request.headers,
            'service_name': os.environ.get('CURRENT_MODULE_ID', '(running locally)'),
            'environment':  os.environ}
    return render_template('index.html', data=data)
'''
END DEFAULT
'''

'''
START GENDATA: Handlers to generate data on the Search API
'''
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
@app.route('/task_gendata/<int:requests>')
def task_generate_data(requests=0):
    
    url = 'https://python27-api-search-dot-grauj-gcp.appspot.com/single_urlfetch' + str(requests -1)
    
    for i in range(_TASKS_TO_CREATE):
        task = taskqueue.add(
            method='GET',
            url='/gendata',
            target='python27-api-search',
            queue_name='search-api'
        )

        if _LOAD_TEST:
            if requests == 0: 
                return "Done with the load testing"

            try:
                rpc = urlfetch.create_rpc(deadline=601)
                urlfetch.make_fetch_call(rpc, url)
            except urlfetch.Error as e:
                import traceback
                traceback.print_exc()

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
@app.route('/batch_task_gendata/<int:requests>')
def batch_task_generate_data(requests=0):
    
    url = 'https://python27-api-search-dot-grauj-gcp.appspot.com/batch_urlfetch/' + str(requests -1)
    
    for i in range(_TASKS_TO_CREATE_BATCH):
        task = taskqueue.add(
            method='GET',
            url='/batch_gendata',
            target='python27-api-search',
            queue_name='search-api'
        )

        if _LOAD_TEST:
            if requests == 0:
                return "Done with the load testing"

            try:
                rpc = urlfetch.create_rpc(deadline=601)
                urlfetch.make_fetch_call(rpc, url)
            except urlfetch.Error as e:
                import traceback
                traceback.print_exc()

    return "Created task with name {} on queue {} targeting {}".format(task.name, task.queue_name, task.target)


@app.route('/single_urlfetch/<requests>')
def single_urlfetch(requests):

    url = 'https://python27-api-search-dot-grauj-gcp.appspot.com/task_gendata' + str(requests)
    
    # Give some time inbetween requests for the application to scale
    time.sleep(_TIME_BETWEEN_REQUESTS)

    try:
        result = urlfetch.fetch(url)
    except urlfetch.Error as e:
        import traceback
        traceback.print_exc()
    finally:
        return "Fetching URL: " + url


@app.route('/batch_urlfetch/<requests>')
def batch_urlfetch(requests):

    url = 'https://python27-api-search-dot-grauj-gcp.appspot.com/batch_task_gendata/' + str(requests)

    # Give some time inbetween requests for the application to scale
    time.sleep(_TIME_BETWEEN_REQUESTS)

    try:
        result = urlfetch.fetch(url)
    except urlfetch.Error as e:
        import traceback
        traceback.print_exc()
    finally:
        return "Fetching URL: " + url
'''
END GENDATA
'''


'''
START QUERY + UPDATE DATA: Handlers to query and update the Search API's data
'''
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
'''
END QUERY + UPDATE DATA
'''

if __name__ == '__main__':
    app.run('127.0.0.1', port=8080, debug=True)

