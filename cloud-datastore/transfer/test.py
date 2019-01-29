from google.cloud import datastore
client = datastore.Client()

task = datastore.Entity(
            client.key('Book','asdasd', namespace='test-three')
        )
client.put(task)

query = client.query(kind='__namespace__')
query.keys_only()



all_namespaces = [entity.key.id_or_name for entity in query.fetch()]

# Filtered namespaces
start_namespace = client.key('__namespace__', 'g')
end_namespace = client.key('__namespace__', 'h')
query = client.query(kind='__namespace__')
query.key_filter(start_namespace, '>=')
query.key_filter(end_namespace, '<')

filtered_namespaces = [entity.key.id_or_name for entity in query.fetch()]


print(all_namespaces, filtered_namespaces)
