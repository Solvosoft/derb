Derb 
=========

**Work in progress**

Documentation_.

.. _Documentation: http://derb.readthedocs.io/en/latest/

Installation 
''''''''''''''


**Clone the repository**

.. code:: bash

	git clone https://github.com/solvo/derb.git
	cd derb

**Set up postgres database (require libpq-dev for psycopg2 compillation)**

Postgres is a requirement, because we use JSONField_.

.. _JSONField: https://docs.djangoproject.com/en/1.10/ref/contrib/postgres/fields/#django.contrib.postgres.fields.JSONField

**Install requirements (require python3-dev for compilation)**

.. code:: bash

	apt-get install python3-dev

Install rabbitmq-server for send emails notifications

.. code:: bash

	apt-get install rabbitmq-server

.. code: bash
	
	pip install -r requirements.txt

* Run migrations

.. code:: bash
	
	python manage.py migrate

* Run developement project

First run in separated terminal an email client 

.. code:: bash

	python -m smtpd -n -c DebuggingServer localhost:1025

Then run in the other terminal 

.. code:: bash

	python manage.py runserver

