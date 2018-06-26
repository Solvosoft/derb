Testing
#######

The Derb project provides a set of unit tests written to guarantee the quality of the code provided, which includes
the validation of different scenarios for the system.

If you want to execute all of the test sets written for the Derb system, you need to run this command from the root
directory of the Django project:

.. code:: bash

    $ python manage.py test

If you want to execute only the test sets written for the base question type views, you have to run this command instead:

.. code:: bash

    $ python manage.py test report_builder.Question.tests

if you want to execute only the test sets written for an specific question type, you have to run this command
(for instance, boolean question):

.. code:: bash

    $ python manage.py test report_builder.Question.QuestionType.tests.test_boolean_question


Troubleshooting
===============

In case you find yourself caught in an exception that says that the user you are using to connect to the PostgreSQL DBMS
doesn't have enough privileges to create a test database, you need to grant those permissions in the PostgreSQL shell.
To do so, run the next command:

.. code:: bash

    $ sudo su postgres
    # Enter your current user password

    $ psql
    psql (9.4.8)
    Type «help» to get help.

    postgres=# ALTER USER derb CREATEDB;
    ALTER ROLE
    postgres=# \q