from flask import Flask, request, render_template

import os


app=Flask(__name__)


@app.route('/')
def index():
    data = {'headers':      request.headers,
            'service_name': os.environ.get('GAE_SERVICE', '(running locally)'),
            'environment':  os.environ}

    return render_template('index.html', data=data)


@app.route('/redis')
@app.route('/memorystore')
def get_memorystore():
    '''
    The responses object are of long-running google.api_core.operation type:
        https://github.com/googleapis/google-cloud-python/blob/6b5218b20d3fa69c96f9690eac07f5a92d13b255/redis/google/cloud/redis_v1/gapic/cloud_redis_client.py#L640
        
    '''
    from google.cloud import redis_v1

    project_id=os.environ.get('GOOGLE_CLOUD_PROJECT', '')
    location='us-central1'
    instance_name=os.environ.get('_MEMORYSTORE_INSTANCE', 'gae-redis')

    print(project_id, location, instance_name)

    try:
        client = redis_v1.CloudRedisClient()

        name = client.instance_path(project_id, location, instance_name)

        instance = client.get_instance(name)

        print(instance)

    except Exception as e:
        import traceback
        print (traceback.print_exc())

        try:
            from google.cloud.redis_v1 import enums

            parent = client.location_path(project_id, location)

            tier = enums.Instance.Tier.BASIC

            memory_size_gb = 1

            instance_settings = {'tier': tier, 
                                 'memory_size_gb': memory_size_gb,
                                 'authorized_network': 'projects/{}/global/networks/serverless'.format(project_id)}

            response = client.create_instance(parent=parent, instance_id=instance_name, instance=instance_settings)
            
            # This should wait until the operation is completed synchronously
            result = response.result()

            instance = client.get_instance(name)

        except Exception as e:
            import traceback
            print(traceback.print_exc())
            return str(e)

    try:
        print("Redis library:")
        import redis

        r = redis.Redis(host=instance.host, port=instance.port, db=0)
        print('Hi redis')
        info = r.info()
        return render_template('redis.html', data=info)

    except:
        import traceback
        return traceback.print_exc()

    return "hi"


@app.route('/cloud_sql')
def cloud_sql():
    pass


if __name__ == '__main__':
    app.run('127.0.0.1', port=8080, debug=True)

