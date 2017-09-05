install:
	while read p; do
	  pip install $p
	done < requirements.pip

windows-rqworker:
<<<<<<< HEAD
	python manage.py rqworker --worker-class simpleworker.SimpleWorker default

runworkers:
	python manage.py rqscheduler && python manage.py rqworker high default
=======
	python manage.py rqworker --worker-class simpleworker.SimpleWorker high default
>>>>>>> ab0ee2ffe39636057c4dbca23b54f9b457fbebe4
