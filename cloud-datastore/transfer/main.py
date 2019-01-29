from google.cloud import datastore
import pprint

client = datastore.Client()
query = client.query(kind='Book')


pprint.pprint(list(query.fetch())[0].id)
