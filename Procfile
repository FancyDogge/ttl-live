web: gunicorn MyTaskTracker.wsgi --log-file -
worker: python manage.py qcluster --settings=MyTaskTracker.settings