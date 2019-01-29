from google.cloud import storage
import wget
import io, os

img_url = 'http://www.hospiceofmontezuma.org/wp-content/uploads/2017/10/confused-man.jpg'

filename = wget.download(img_url)

client = storage.Client()
bucket = client.get_bucket('buckete')
blob = bucket.blob('image.jpg')

blob.upload_from_filename(filename, content_type='image/jpg')
os.remove(filename)
