from google.oauth2 import service_account
import googleapiclient.discovery


credentials = service_account.Credentials.from_service_account_file(
    filename='key.json',
    scopes=['https://www.googleapis.com/auth/cloud-platform'])

service = googleapiclient.discovery.build(
    'cloudresourcemanager', 'v1', credentials=credentials)


if __name__ == "__main__":
    project_id="inlaid-isotope-241210"
    policy=service.projects().getIamPolicy(
                resource=project_id,
                body={},
            ).execute()
    for member in policy['bindings']:
        print (member['role'])
