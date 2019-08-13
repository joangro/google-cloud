from google.cloud.spanner.pool import AbstractSessionPool

class CustomSpannerPool(AbstractSessionPool):
    def __init__(self, custom_param):
        super(MyCustomPool, self).__init__()
        self.custom_param=custom_param
    

