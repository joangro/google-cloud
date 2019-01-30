from google.oauth2 import service_account
import googleapiclient.discovery


credentials = service_account.Credentials.from_service_account_file(
    filename='/home/grauj/key.json',
    scopes=['https://www.googleapis.com/auth/cloud-platform'])
service = googleapiclient.discovery.build(
            'dataflow', 'v1b3', credentials=credentials)




project_id="wave16-joan"
job_id="2019-01-28_08_42_13-12253286524790826336"

messages=service.projects().jobs().messages().list(
            projectId=project_id,
            jobId=job_id
        ).execute()

try:
    print("Current number of workers is "+messages['autoscalingEvents'][-1]['currentNumWorkers'])
except:
    print("Current number of workers is 0")
