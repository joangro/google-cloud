If you want to fully automatize this process, I would do the following:

1. **Create a [Cloud Function](https://cloud.google.com/functions/) to handle the export**:

This is the more lightweight solution, as Cloud Functions are serverless, and  provide flexibility to implement code with the [Client Libraries](https://cloud.google.com/bigquery/docs/reference/libraries). See the [quickstart](https://cloud.google.com/functions/docs/quickstart-console), I recommend you to use the console to create the functions to start with. 

In this example I recommend you to trigger the Cloud Function [from an HTTP request](https://cloud.google.com/functions/docs/calling/http), i.e. when the function URL is called, it will run the code inside of it. 

An example Cloud Function code in Python, that creates the export when a HTTP request is made:

**main.py**

    from google.cloud import bigquery
    
    def hello_world(request):
        project_name = "MY_PROJECT"
        bucket_name = "MY_BUCKET"
        dataset_name = "MY_DATASET"
        table_name = "MY_TABLE"
        destination_uri = "gs://{}/{}".format(bucket_name, "bq_export.csv.gz")
        
        bq_client = bigquery.Client(project=project_name)
        
    	dataset = bq_client.dataset(dataset_name, project=project_name)
        table_to_export = dataset.table(table_name)
        
        job_config = bigquery.job.ExtractJobConfig()
        job_config.compression = bigquery.Compression.GZIP
        
        extract_job = bq_client.extract_table(
            table_to_export,
            destination_uri,
            # Location must match that of the source table.
            location="US",
            job_config=job_config,
        )  
        return "Job with ID {} started exporting data from {}.{} to {}".format(extract_job.job_id, dataset_name, table_name, destination_uri)

**requirements.txt**

    google-cloud-bigquery

Note that the job will run asynchronously in the background, you will receive a return response with the job ID, which you can use to check the state of the export job in the Cloud Shell, by running:

    bq show -j <job_id>

2. **Create a [Cloud Scheduler](https://cloud.google.com/scheduler/) scheduled job**:

Follow this [documentation](https://cloud.google.com/scheduler/docs/creating) to get started. You can set the Frequency with the [standard cron format](https://en.wikipedia.org/wiki/Cron), for example `0 0 * * *` will run the job   every day at midnight.

As a target, choose `HTTP`, in the URL put the Cloud Function HTTP URL (you can find it in the console, inside the Cloud Function details, under the Trigger tab), and as `HTTP method` choose `GET`.

Create it, and you can test it in the Cloud Scheduler by pressing the `Run now` button in the Console.

3. **Synchronize your external server and the bucket**:

Up until now you only have scheduled exports to run every 24 hours, now to synchronize the bucket contents with your local computer, you can use the [`gsutil rsync`](https://cloud.google.com/storage/docs/gsutil/commands/rsync) command. If you want to save the imports, lets say to the `my_exports` folder, you can run, in your external server:

    gsutil rsync gs://BUCKET_WITH_EXPORTS /local-path-to/my_exports

To periodically run this command in your server, you could create a standard [cron job in your crontab](https://linuxize.com/post/scheduling-cron-jobs-with-crontab/) inside your external server, to run each day as well, just at a few hours later than the bigquery export, to ensure that the export has been made.


**Extra**:

I have hard-coded most of the variables in the Cloud Function to be always the same. However, you can send parameters to the function, if you do a `POST` request instead of a `GET` request, and send the parameters as data in the body.

You will have to change the Cloud Scheduler job to send a `POST` request to the Cloud Function HTTP URL, and in the same place you can set the body to send the parameters regarding the `table`, `dataset` and `bucket`, for example. This will allow you to run exports from different tables at different hours, and to different buckets.



