from flask import Flask, request, render_template
import os
import requests


app = Flask(__name__)


@app.route('/')
def print_headers():
    data = {'headers':      request.headers,
            'service_name': os.environ.get('CURRENT_MODULE_ID', '(running locally)'),
            'environment':  os.environ}
    return render_template('index.html', data=data)


@app.route('/pingme/<num_requests>')
def ping(num_requests):
    import time
    if int(num_requests) == 0:
        return "Done!"
    else:
        for i in range(2):
            requests.get('https://spammer-k5uvdhldwa-uc.a.run.app/pingme/{}'.format(str(int(num_requests) -1)))
            time.sleep(1)

        return "ok"


if __name__ == '__main__':
    app.run('0.0.0.0', port=8080, debug=True)

