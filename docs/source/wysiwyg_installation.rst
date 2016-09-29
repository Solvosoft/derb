Wysiwyg installation with CKEditor
##############################

Follow this steps for installation of Wysiwyg files with CKEditor.

Dependencies
============

* Install packages: Via pip, you must install your platform’s packages (Linux, Debian/Ubuntu).

.. code-block:: bash

     pip install django-wysiwyg


* Configuration: Add ‘django_wysiwyg’ to your INSTALLED_APPS in settings.py:

.. code-block:: bash

    INSTALLED_APPS = (
    ...
    'django_wysiwyg',
    )

Using the CKEditor
====

* If you wish to use CKEditor set the flavor in settings.py:

.. code-block:: bash

    DJANGO_WYSIWYG_FLAVOR = "ckeditor"

* Install packages: Via pip.

.. code-block:: bash

     pip install django-ckeditor

* Configuration: Add ‘ckeditor’ to your INSTALLED_APPS in settings.py:

.. code-block:: bash

    INSTALLED_APPS = (
    ...
    'ckeditor'
    )

* Configuration of the media and static path: Add at at the final in settings.py:

.. code-block:: bash

   STATIC_ROOT = os.path.join(BASE_DIR, 'static/')

.. code-block:: bash

   STATIC_ROOT = os.path.join(BASE_DIR, 'media/')


Code
====

* You need to define a HTML template ("example_wysiwyg.html"). 

.. code-block:: bash

    {% load wysiwyg %}
    {% wysiwyg_setup %}

	<textarea id="foo"></textarea>

    {% wysiwyg_editor "foo" %}
