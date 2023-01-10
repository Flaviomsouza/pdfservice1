import os

import redis
from rq import Worker, Queue, Connection

listen = ['high', 'default', 'low']

redis_url = os.getenv('REDIS_URL', os.environ['REDIS_URL'])

conn = redis.Redis(decode_responses=False, host=os.environ['REDIS_HOST'], username=os.environ['REDIS_USERNAME'], password=os.environ['REDIS_PASSWORD'], port=15022)


if __name__ == '__main__':
    with Connection(conn):
        worker = Worker(map(Queue, listen))
        worker.work()
