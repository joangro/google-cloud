from google.cloud import logging
from google.cloud.logging.resource import Resou
log_client = logging.Client()
log_name = 'projects/{}/logs/cloudfunctions.googleapis.com%2Fcloud-functions' # Example creates a log under cloud functions resource
res = Resource(type="cloud_function", 
               labels={
                   "function_name": "CLOUD-FUNCTION-NAME", 
                   "region": "CLOUD-FUNCTION-LOCATION"
               },
              )
logger = log_client.logger(log_name.format("MY-PROJECT-NAME"))
logger.log_struct(
 {"message": "hi"}, resource=res, severity='ERROR')

return 'Wrote logs to {}.'.format(logger.name)
