release: python manage.py migrate
web: waitress-serve --port=$PORT dj.wsgi:application
worker: python manage.py rqworker high default low
