install:
	while read p; do
	  pip install $p
	done < requirements.pip

windows-rqworker:
	python manage.py rqworker --worker-class simpleworker.SimpleWorker high default

runworkers:
	python manage.py rqscheduler & python manage.py rqworker high default
