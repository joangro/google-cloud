import jwt, time

import urllib.request

iat = time.time()
exp = iat+3600
payload={'iss': 'example@my-project.iam.gserviceaccount.com',
         'sub': 'example@my-project.iam.gserviceaccount.com',
         'aud': 'https://datastore.googleapis.com/google.datastore.admin.v1.DatastoreAdmin',
         'iat': iat,
         'exp': exp}

additional_headers={'kid': 'Private-Key-Id'}

PK = b'-----BEGIN PRIVATE KEY-----\nPRIVATE-KEY-BODY\n-----END PRIVATE KEY-----'

signed_jwt = jwt.encode(payload, PK, headers=additional_headers, algorithm='RS256')

print(additional_headers['kid'])
print(signed_jwt)

req = urllib.request.Request("https://datastore.googleapis.com/v1/projects/my-project/indexes",headers={"Authorization": "Bearer {}".format(signed_jwt.decode("UTF-8")), "Host": "datastore.googleapis.com"}, method='GET')

res = urllib.request.urlopen(req)
time.sleep(2)
print(res.read())
