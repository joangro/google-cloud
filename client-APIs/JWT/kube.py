
import urllib.request
import googleapiclient.discovery
import base64, pprint
import kubernetes.client
from google.oauth2 import service_account


credentials = service_account.Credentials.from_service_account_file("key.json")
gke = googleapiclient.discovery.build('container', 'v1', credentials=credentials)
name = 'projects/wave16-joan/locations/us-central1-a/clusters/standard-cluster-1'
gke_clusters = gke.projects().locations().clusters()
gke_cluster = gke_clusters.get(name=name).execute()

kube_config = kubernetes.client.Configuration()
kube_config.host = 'https://{}'.format(gke_cluster['endpoint'])
kube_config.verify_ssl = True

kube_config.api_key['authorization'] = '-----'
kube_config.api_key_prefix['authorization'] = 'Bearer'

kube_config.ssl_ca_cert = 'ssl_ca_cert'

with open(kube_config.ssl_ca_cert, 'wb') as f:
    f.write(base64.decodestring(gke_cluster['masterAuth']['clusterCaCertificate'].encode()))

kube_client = kubernetes.client.ApiClient(configuration=kube_config)
kube_v1 = kubernetes.client.CoreV1Api(kube_client)
pprint.pprint(kube_v1.list_pod_for_all_namespaces())

'''
req = urllib.request.Request("https://datastore.googleapis.com/v1/projects/wave16-joan/indexes",headers={"Authorization": "Bearer {}".format(signed_jwt.decode("UTF-8")), "Host": "datastore.googleapis.com"}, method='GET')

res = urllib.request.urlopen(req)
time.sleep(2)
print(res.read())
'''
