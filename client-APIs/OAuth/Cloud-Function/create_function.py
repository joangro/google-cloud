import httplib2
import pprint

from googleapiclient.discovery import build
from oauth2client.service_account import ServiceAccountCredentials


credentials = ServiceAccountCredentials.from_json_keyfile_name(
                
                "key.json",
                scopes="https://www.googleapis.com/auth/cloud-platform")

http = httplib2.Http()
http = credentials.authorize(http)

service = build("cloudfunctions", "v1", http=http)

lists = service.projects().locations().functions().create(
            location='projects/wave16-joan/locations/europe-west1',
            body={
                    "name":"...",
                    "entryPoint":"..."
                    "httpsTrigger": {
                            "url":"..."
                        }
                }
        )

pprint.pprint(lists)
