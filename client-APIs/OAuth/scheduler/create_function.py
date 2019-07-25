import httplib2
import pprint

from googleapiclient.discovery import build
from oauth2client.service_account import ServiceAccountCredentials


credentials = ServiceAccountCredentials.from_json_keyfile_name(
                "key-scheduler.json",
                scopes=["https://www.googleapis.com/auth/cloud-platform"])

http = httplib2.Http()
http = credentials.authorize(http)

service = build("cloudbuild", "v1", http=http)

lists = service.projects().triggers().run(
            projectId='wave16-joan',
            triggerId='6f089d5a-853e-49ae-836d-824a7c819972',
            body={
                    "branchName":"master",
                }
        ).execute()

pprint.pprint(lists)
