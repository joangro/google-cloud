from google.cloud import tasks_v2beta3
import argparse

def createQueue(name):
    queue = {"name": "projects/{}/locations/{}/queues/{}".format(args.project, args.location, name),
            }
    
    client.create_queue(parent, queue)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
                description='Create queue for cloud tasks')
    parser.add_argument('-p','--project',required=True,type=str,
                        help='Project name where the queue will be created.')
    parser.add_argument('-lo','--location',default='europe-west1',type=str,
                        help='Location where the application is running')
    parser.add_argument('-n','--name',required=True,type=str,
                        help='Queue name')
    args = parser.parse_args()

    try:
        client = tasks_v2beta3.CloudTasksClient()
    except:
        print('Couldn\'t create client. Check project parameters.')
    
    try:
        parent = client.location_path(args.project, args.location)
    except:
        print('Could not create parent with input project and location')
    

    createQueue(args.name)
