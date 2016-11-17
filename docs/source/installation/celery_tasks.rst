Celery tasks
############

This guide will help you understand how to run tasks asynchronously with celery, using the Python package called ``async_notifications``.

Dependencies
============

You have to install system and Python requirements to be able to run celery tasks properly.

* System dependencies: in the ``derb`` project the tasks are run to trigger email notifications, so we need support in the operating system for a worker that takes care of those requests accordingly. In the case of this project, we use RabbitMQ (https://www.rabbitmq.com/). To install the worker server, install the next packages according to your Linux distro:

 * Debian:

 .. code-block:: bash

    $ sudo apt-get install rabbitmq-server

* Python dependencies: in the ``derb`` you can find a requirements file which includes the Python to use the async_notifications package. Go to the Installation section to see how to install the Python requirements of the project using the virtual environment. If you want to install the Celery requirements manually run this:

.. code-block:: bash

    $ pip install celery=3.1.23 async-notifications==0.0.3

Run in debug mode
=================

To setup an environment to test the async_notifications package funcionality, you need three shell sessions.

1. Run the SMTP debug client:

.. code-block:: bash

    $ python -m smtpd -n -c DebuggingServer localhost:1025

2. Run celery with the ``derb`` project. If you haven't setup celery yet, see `celery documentation <http://docs.celeryproject.org/en/latest/django/first-steps-with-django.html>`_.

.. code:: bash

    $ celery -A derb worker -l info -B

3. Run the Django webserver in development

.. code:: bash

    $ python manage.py runserver

More info
=========

If you need more info about how to use async_notifications packages, please refer to its `Github page <https://github.com/luisza/async_notifications>`_.