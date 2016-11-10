Derb: Django Enterprise Report Builder 
===========================================

|build-status| |license| |djangoversion| |pyversion| |developby| 

This software is in development state, it's not stable yet 

Documentation
---------------------

See Documentation_.

.. _Documentation: http://derb.readthedocs.io/en/latest/

Installation 
---------------

* clone the repository

.. code:: bash

    git clone https://github.com/solvo/derb.git
    cd derb

* Set up postgres database (require libpq-dev for psycopg2 compillation)

Postgres is a requirement, because we use JSONField_

.. _JSONField: https://docs.djangoproject.com/en/1.10/ref/contrib/postgres/fields/#django.contrib.postgres.fields.JSONField

* Install requirements (require python3-dev for compilation)

Install rabbitmq-server for send emails notifications

.. code:: bash

	apt-get install rabbitmq-server

.. code:: bash
	
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


.. |build-status| image:: https://api.travis-ci.org/solvo/derb.png?branch=development
    :alt: Build status
    :target: https://travis-ci.org/solvo/derb

.. |license| image:: https://img.shields.io/badge/license-GPLv3-green.svg
    :alt: GPL v3
    :target: https://www.gnu.org/licenses/gpl-3.0.en.html

.. |djangoversion| image:: https://img.shields.io/badge/Django-v1.10-blue.svg
    :alt: Django vesion 1.10
    :target: https://docs.djangoproject.com/en/1.10/

.. |pyversion| image:: https://img.shields.io/badge/Python-v3.4,3.5-green.svg
    :alt: Supported Python versions.
    :target: #

.. |developby| image:: https://img.shields.io/badge/Develop%20by-Solvo-orange.svg
    :alt: Supported Python versions.
    :target: https://solvosoft.com


