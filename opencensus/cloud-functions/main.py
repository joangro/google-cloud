from opencensus.ext.stackdriver import trace_exporter as stackdriver_exporter
import opencensus.trace.tracer
import os

def initTracer():
    '''
    Init required trace objects
    '''
    project_id = os.environ.get('GCP_PROJECT')
    
    exporter = stackdriver_exporter.StackdriverExporter(
                    project_id=project_id
                )
    
    tracer = opencensus.trace.tracer.Tracer(
                    exporter=exporter,
                    sampler=opencensus.trace.tracer.samplers.AlwaysOnSampler()
                )
    return tracer


def trace_requests(request):
    """Responds to any HTTP request.
    Args:
        request (flask.Request): HTTP request object.
    Returns:
        The response text or any set of values that can be turned into a
        Response object using
        `make_response <http://flask.pocoo.org/docs/1.0/api/#flask.Flask.make_response>`.
    """
    tracer = initTracer()

    base_name = os.environ.get("FUNCTION_NAME") + "-trace-"

    with tracer.span(name=base_name + "metadata-call"):

        import requests

        r = requests.get("http://metadata.google.internal/computeMetadata/v1/project/numeric-project-id",
                         headers={'Metadata-Flavor': 'Google'})


    return r.content

