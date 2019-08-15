from google.cloud.spanner import Client
from google.cloud.spanner_v1.pool import TransactionPingingPool

_INSTANCE_NAME='testing'
_DATABASE_NAME='test'

if __name__=='__main__':
    client = Client()

    instance = client.instance(_INSTANCE_NAME)

    custom_pool = TransactionPingingPool(size=1000, default_timeout=5, ping_interval=300)

    database = instance.database(_DATABASE_NAME, pool=custom_pool)
