web: gunicorn --pythonpath="$PWD/dj" config.wsgi:application
worker: python dj/manage.py rqworker high default low

