from google.cloud import scheduler_v1beta1

client = scheduler_v1beta1.CloudSchedulerClient()

project = "my-project-name"

location = "europe-west1"

name = "my-job-nameb"

parent = client.location_path(project, location)

job = {
  "name": "projects/{}/locations/{}/jobs/{}".format(project, location, name),
  "description": "Test",
  "schedule": "* * * * *",
  "time_zone": "UTC",
    "http_target": 
  {
    "http_method": "GET",
    "uri": "https://google.com"
  }


}

response = client.create_job(parent, job)
