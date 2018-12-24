from google.cloud import scheduler_v1beta1

client = scheduler_v1beta1.CloudSchedulerClient()

parent = client.location_path('joan-grau-2018','europe-west1')
        
job = {
  "name": "projects/joan-grau-2018/locations/europe-west1/jobs/test-job-correct",
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
