web: waitress-serve --port=$PORT dj.wsgi:application
worker: python dj/manage.py rqworker high default low

