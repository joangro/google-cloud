import urllib.request
from google.cloud import storage

source_file_name = 'http://www.hospiceofmontezuma.org/wp-content/uploads/2017/10/confused-man.jpg'

link = urllib.request.urlopen(source_file_name)

client = storage.Client()
bucket = client.get_bucket('buckete')
blob = bucket.blob('image2.jpg')

blob.upload_from_string(link.read(), content_type='image/jpg')

