from flask import Flask, request, render_template

import os

app=Flask(__name__)

@app.route('/')
def index():
    data = {'headers':      request.headers,
            'service_name': os.environ.get('CURRENT_MODULE_ID', '(running locally)'),
            'environment':  os.environ}
    return render_template('index.html', data=data)


if __name__ == '__main__':
    app.run('127.0.0.1', port=8080, debug=True)
