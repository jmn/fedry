import os

import redis
from rq import Queue, Connection
from rq.worker import HerokuWorker as Worker
from django.conf import settings
import django
django.setup()

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dj.settings.production')

listen = ['high', 'default', 'low']

redis_url = os.getenv('REDIS_URL', 'redis://localhost:6379')

conn = redis.from_url(redis_url)

if __name__ == '__main__':
    with Connection(conn):
        worker = Worker(map(Queue, listen))
        worker.work()
