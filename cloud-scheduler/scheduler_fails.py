from google.cloud import scheduler_v1beta1

client = scheduler_v1beta1.CloudSchedulerClient()

project = "my-project-id"

location = "europe-west1"

name = "my-job-name"

parent = client.location_path(project, location)
        
job = {
  "name": "projects/{}/locations/{}/jobs/{}".format(project, location, name),
  "description": "Test",
  "schedule": "* * * * *",
  "http_target": 
  {
    "http_method": "GET",
    "uri": "https://google.com"
  }


}

response = client.create_job(parent, job)
