runserver:
	python3 weather_app/manage.py runserver

migrate:
	python3 weather_app/manage.py makemigrations
	python3 weather_app/manage.py migrate

testing:
	python3 weather_app/manage.py test weather_app.weather.tests