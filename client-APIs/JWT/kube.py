
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

kube_config.api_key['authorization'] = 'eyJhbGciOiJSUzI1NiIsImtpZCI6IiJ9.eyJpc3MiOiJrdWJlcm5ldGVzL3NlcnZpY2VhY2NvdW50Iiwia3ViZXJuZXRlcy5pby9zZXJ2aWNlYWNjb3VudC9uYW1lc3BhY2UiOiJkZWZhdWx0Iiwia3ViZXJuZXRlcy5pby9zZXJ2aWNlYWNjb3VudC9zZWNyZXQubmFtZSI6ImRlZmF1bHQtdG9rZW4tc202bTIiLCJrdWJlcm5ldGVzLmlvL3NlcnZpY2VhY2NvdW50L3NlcnZpY2UtYWNjb3VudC5uYW1lIjoiZGVmYXVsdCIsImt1YmVybmV0ZXMuaW8vc2VydmljZWFjY291bnQvc2VydmljZS1hY2NvdW50LnVpZCI6IjFmYzQyZTU0LTI4OGYtMTFlOS05OThiLTQyMDEwYTgwMDBhZiIsInN1YiI6InN5c3RlbTpzZXJ2aWNlYWNjb3VudDpkZWZhdWx0OmRlZmF1bHQifQ.bT1PFkV901-XSSuqFeSVeufixF3VfHrTPI0or6hqSKIPvGhE9d6H57JvroPoebOIOTP-PvLHH_760kQN5cw4AHL-_0MntaE98cJOy4Et97xrT_buHN-t-XXkBtO1J1miy_jmUNAkv1WAEwHE0Q2y7FpwasQRHrEhErRoqSFIEzaV9_HflB0kgiD13XnzxX08SkYx9_CktirsB3QCxV6uHLPhFdpExTPHKdqvaRPzomGpoOryqEUqWsr9zqSF0-HhbbflWPzpVhXIEYyJ4RGJCUH1P8qMlU2n0j3kMBgMvhb8ujJntWw--9uoupRJkeIB2cbrCu5fvDBtF7E-hZFWuQ'
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
