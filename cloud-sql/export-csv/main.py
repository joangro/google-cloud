from flask import Flaski, request
from pprint import pprint

from googleapiclient import discovery
from oauth2client.client import GoogleCredentials


app = Flask(__name__)

@app.route('/')
def hello():
    return 'Hello World!'


@app.route('/sql')
def sql():
    '''
        You will have to run `gcloud beta auth application-default login` to provide
        credentials to the application
    '''
    credentials = GoogleCredentials.get_application_default()
    service = discovery.build('sqladmin', 'v1beta4', credentials=credentials)
    
    table = request.args.get('table', default = 'hold_table', type=str)
    try:
        my-query = request.args.get('query')
    except:
        print('Specify a query in the \'query\' parameter')
        
    # TODO
    project = 'YOUR-PROJECT'
    instance = 'YOUR-CLOUDSQL-INSTANCE'
    bucket-name = 'YOUR-CLOUD-STORAGE-BUCKET (gs://example)'
    save-name = 'YOUR-FILE-SAVE-NAME'
    # ENDTODO

    instances_export_request_body = {
        "exportContext": {
            "csvExportOptions": {
                "selectQuery": my-query,
            },
            "databases": ["import"],
            "fileType": "CSV",
            "uri": "{}/{}".format(bucket-name, save-name),
            "kind": "sql#exportContext"
            }
        }

    request = service.instances().export(project=project, instance=instance, body=instances_export_request_body)
    response = request.execute()
    pprint(response)
    return 'OK. Status: '+response["status"] 

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)

