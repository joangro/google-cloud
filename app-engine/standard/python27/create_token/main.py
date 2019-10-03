from google.appengine.api import app_identity

import google.auth
import google.auth.iam
import google.auth.app_engine
import google.oauth2.credentials
import google.oauth2.service_account
from google.auth.transport.requests import Request

import requests
import requests_toolbelt.adapters.appengine

from flask import Flask

app = Flask(__name__)

cf_name = 'https://us-central1-grauj-gcp.cloudfunctions.net/require-authentication'
OAUTH_TOKEN_URI = 'https://www.googleapis.com/oauth2/v4/token'

@app.route('/')
def create_token():
    credentials, _ = google.auth.default(
        scopes=[cf_name])
    
    requests_toolbelt.adapters.appengine.monkeypatch()

    signer_email = credentials.service_account_email

    signer = credentials.signer

    service_account_credentials = google.oauth2.service_account.Credentials(
            signer, signer_email, token_uri=OAUTH_TOKEN_URI, additional_claims={
                'target_audience': cf_name
            })

    service_account_jwt = (
            service_account_credentials._make_authorization_grant_assertion())

    request = google.auth.transport.requests.Request()
    body = {
            'assertion': service_account_jwt,
            'grant_type': google.oauth2._client._JWT_GRANT_TYPE,
        }
    token = google.oauth2._client._token_endpoint_request(
            request, OAUTH_TOKEN_URI, body)

    print(token['id_token'])

    resp = requests.request(
            'GET', cf_name,
            headers={'Authorization': 'Bearer {}'.format(token['id_token'])}
            )

    return resp.text


if __name__ == '__main__':
    app.run('127.0.0.1', port=8080, debug=True)
