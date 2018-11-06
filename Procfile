release: python manage.py migrate
web: waitress-serve --port=$PORT dj.wsgi:application
# worker: python manage.py rqworker high default low
worker: python worker.py
scheduler: python manage.py rqscheduler
