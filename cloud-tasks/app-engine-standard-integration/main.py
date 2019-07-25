# Copyright 2018 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""App Engine app to serve as an endpoint for App Engine queue samples."""
from flask import Flask, request
from google.cloud import tasks_v2beta3
from google.protobuf import timestamp_pb2
import datetime, time

app = Flask(__name__)


@app.route('/example_test_handler', methods=['POST'])
def example_test_handler():
    """Log the request payload."""
    payload = request.get_data(as_text=True) or '(empty payload)'
    print('Received task with payload: {}'.format(payload))
    
    return payload

@app.route('/create_task', methods=['POST'])
def create_task():
    client = tasks_v2beta3.CloudTasksClient()
    parent = client.queue_path('wave16-joan', 'europe-west2', 'newQueue')
    task = {
            'app_engine_http_request': {
                'http_method': 'POST',
                'relative_uri': '/example_test_handler',
                'headers': [("Content-Type", "application/json")],
                'app_engine_routing': {
                    'service': 'tasks-standard'
                },
                'body': str.encode('hi')
            }
    }
    print("task created")
    d = datetime.datetime.utcnow() + datetime.timedelta(seconds=3)
    timestamp = timestamp_pb2.Timestamp()
    timestamp.FromDatetime(d)
    task['schedule_time'] = timestamp
    response = client.create_task(parent, task)
    return "Task Created"

@app.route('/')
def hello():
    """Basic index to verify app is serving."""
    return 'Hello World!'


if __name__ == '__main__':
    # This is used when running locally. Gunicorn is used to run the
    # application on Google App Engine. See entrypoint in app.yaml.
    app.run(host='127.0.0.1', port=8080, debug=True)
