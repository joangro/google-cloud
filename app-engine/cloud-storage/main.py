from flask import Flask
from google.cloud import storage


# If `entrypoint` is not defined in app.yaml, App Engine will look for an app
# called `app` in `main.py`.
app = Flask(__name__)


@app.route('/')
def hello():
    """Return a friendly HTTP greeting."""
    return 'Hello World!'

@app.route('/openFile')
def openFile():
    client = storage.Client()
    bucket = client.get_bucket('buckete')
    blob = bucket.get_blob('docker-sql-admin/wave16-joan-2ab85fbc2164.json')
    return blob.download_as_string()

if __name__ == '__main__':
    # This is used when running locally only. When deploying to Google App
    # Engine, a webserver process such as Gunicorn will serve the app. This
    # can be configured by adding an `entrypoint` to app.yaml.
    app.run(host='127.0.0.1', port=8080, debug=True)
# [END gae_python37_app]wq

