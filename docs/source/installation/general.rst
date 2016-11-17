General Installation
########################

Clone this repository

.. code-block:: bash

    $ cd ~/projects/
    $ git clone git@github.com:solvo/derb.git
    $ cd derb

Create a virtualenv

.. code-block:: bash

    $ mkdir -p ~/environments
    $ virtualenv -p python3 ~/environments/derb
    $ source ~/environments/derb/bin/activate

Install system requirements

* Debian:

.. code-block:: bash

    $ sudo apt-get install python-dev libpq-dev

Install Python requirements

.. code-block:: bash

    $ cd ~/projects/derb
    $ pip install -r requirements.txt

Run in development
------------------

Check your database configuration and sync your models

.. code-block:: bash

    $ python manage.py migrate


Create a superuser for admin views

.. code-block:: bash

    $ python manage.py createsuperuser

Run your development server

.. code-block:: bash

    $ python manage.py runserver
