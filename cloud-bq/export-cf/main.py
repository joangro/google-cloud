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

