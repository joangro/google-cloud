from flask import Flask, request, render_template

from google.appengine.api import search

import os

app=Flask(__name__)

@app.route('/')
def index():
    data = {'headers':      request.headers,
            'service_name': os.environ.get('CURRENT_MODULE_ID', '(running locally)'),
            'environment':  os.environ}
    return render_template('index.html', data=data)


@app.route('/gendata')
def generate_data():
    import gen_data
    gen_data.create_index_and_document()
    return "hi"


if __name__ == '__main__':
    app.run('127.0.0.1', port=8080, debug=True)
