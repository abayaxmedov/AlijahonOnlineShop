mig:
	./manage.py makemigrations
	./manage.py migrate

super:
	./manage.py createsuperuser
shell:
	./manage.py shell
run:
	./manage.py runserver
pip:
	pip freeze > requirements.txt
help:
	./manage.py
makemessages:
	python3 manage.py makemessages -l en
	python3 manage.py makemessages -l uz
compile:
	python3 manage.py compilemessages