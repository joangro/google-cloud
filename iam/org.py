from googleapiclient.discovery import build
import google.auth

(credentials, project) = google.auth.default()

service = build('cloudresourcemanager', 'v2', credentials=credentials)

service_projects = build('cloudresourcemanager', 'v1', credentials=credentials)


def listProjects(projects):
    try:
        # try in case that there are no projects here
        for project in projects:
            print("Project under organization: "+project['projectId'])
    except:
        print("No projects under parent")


if __name__ == "__main__":
    org_id="organizations/383705642747"
    parent_folders = service.folders().list(parent=org_id).execute() 

    # First list all the projects under the organization
    parent_projects = service_projects.projects().list(filter="parent.id:{}".format(org_id.split('/')[1])).execute()
    listProjects(parent_projects['projects'])

    # Now, fetch all the folders under the parent folder
    for folder in parent_folders['folders']:
        folder_id = folder['name']
        print("Parent folder name: " + folder_id)
        parent_projects = service_projects.projects().list(filter="parent.id:{}".format(org_id.split('/')[1])).execute()
        listProjects(parent_projects['projects'])
        # Fetch the child folders if there is any. This is only done once, in case that there are more in your org, you can do it recursively
        child_folders = service.folders().list(parent=folder_id).execute()
        try:
            # we do a try in case that there are no child folders
            for child_folder in child_folders['folders']:
                print("Child folder name: " + child_folder['name'])
                projects_under_folder = service_projects.projects().list(filter="parent.id:{}".format(child_folder['name'].split('/')[1])).execute()
                listProjects(projects_under_folder['projects'])
        except:
            continue

