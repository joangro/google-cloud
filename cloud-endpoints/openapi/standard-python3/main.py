from flask import Flask, request
from googleapiclient import discovery
from oauth2client.client import GoogleCredentials
import os, json


app = Flask(__name__)

@app.route('/')
def root():
    return "placeholder, this won't get called by the ESP"

@app.route('/sql', methods=['GET', 'POST'])
def sql():
    credentials = GoogleCredentials.get_application_default()

    service = discovery.build('sqladmin', 'v1beta4', credentials=credentials)

    if request.method == 'GET':

        req = service.instances().list(project=os.environ.get('PROJECT_ID'))
        
        instance_list = []

        while req is not None:
            instances = req.execute()
            
            instance_object = {}

            for instance in instances['items']:
                instance_object['instanceName'] = instance['name']
                instance_object['instanceRegion'] = instance['region']
                instance_object['instanceType'] = instance['databaseVersion']
                instance_list.append(instance_object)

            req = service.instances().list_next(previous_request=req, previous_response=instances)
                
        return json.dumps(instance_list)

        
    if request.method == 'POST':
        data = request.form
        try:
            # Not actually going to create the instance, leaving this as a placeholder
            '''
            database_instance_body = {
                "name": request.form['instanceName'],
                "settings": {
                    "tier": "db-n1-standard-1 ",
                    "dataDiskSizeGb": 10,
                    "dataDiskType": "PD_SSD"
                    },
                "databaseVersion": "MYSQL_5_7"
                }
            req = service.instances().insert(project=os.environ['PROJECT_ID'], body=database_instance_body)
            resp = req.execute()
            '''
            print("hi")
        except Exception:
            return "Bad request", 400

        return "ok"

if __name__=='__main__':
    app.run('127.0.0.1', port=8080, debug=True)
