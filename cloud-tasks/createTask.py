from google.cloud import tasks_v2beta3
import argparse


def createTask():
    task={"app_engine_http_request":{
                "http_method": "POST",
                "relative_uri": "/basic_handler",
            },
        }
    
    if payload:
        encode_payload = payload.encode()
        # Send payload to text as content
        task["app_engine_http_request"]["body"] = encode_payload

    response = client.create_task(parent, task)

    return response


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Create task to a queue')
    
    parser.add_argument('payload',type=str,
                        help='Payload to send to task')
    parser.add_argument('-n','--name',type=str,
                        help='Name of the task')
    parser.add_argument('-q','--queue',type=str,
                        help='Queue where the task will be created')
    parser.add_argument('-p','--project',type=str,
                        help='Project name where to create the task')
    parser.add_argument('-lo','--location',type=str,default='europe-west1',
                        help='Zone where the queue will run (ex, europe-west1)')
    args = parser.parse_args()
    try:
        client = tasks_v2beta3.CloudTasksClient()
    except:
        print('Could not create client')

    try:
        parent = client.queue_path(args.project, args.location, args.queue)
    except:
        print('Could not create the parent')

    createTask()
