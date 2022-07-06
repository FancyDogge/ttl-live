# ttl-live
* [General info](#general-info)
* [Technologies](#technologies)
* [Setup](#setup)

## General info
This is a personal diary/task-tracker app, where you cant create, view, update and delete yoyr tasks.
If your task have a deadline, you will be notified when it's about to reach a deadline.
You can also go to a dashboard, where you will be able to see closest deadlines, paused and finished tasks.
	
## Technologies
Project is created with dajngo and django-q library, check out requirements.txt for more info.
	
## Setup
To run this project, clone it and make sure you're in its directory.
Then you should install requirements, make and apply migrations:

```
pip install -r requirements.txt
py manage.py makemigrations
py manage.py migrate
```

After that you should create superuser if you want an admin account

```
py manage.py createsuperuser
```

When you're done, run qcluster(library for background tasks) in one terminal

```
py manage.py qcluster
```
And local server in the other
```
py manage.py runserver
```

Now have fun!
