from google.cloud import storage
from google.cloud.storage import Blob

def transferFiles(files_to_transfer):
    for fi in files_to_transfer:
        blob_file = Blob(fi, bucket_target)
        blob.upload_from_filename(bucket_origin_name+'/'+fi)

if __name__ == '__main__':
    try:
        client = storage.Client()
    except:
        print('Could not initialize Storage Clien')

    bucket_origin_name = 'origin_bucket'
    bucket_target_name = 'bucket_target'
    files_to_transfer = ['test_file', 'second_file...']

    try: 
        bucket_origin = client.get_bucket(bucket_origin_name)
    except:
        print('Could not fetch origin bucket')

    try: 
        bucket_target = client.get_bucket(bucket_target_name)
    except:
        print('Could not fetch target bucket')
    
    transferFiles(files_to_transfer)

