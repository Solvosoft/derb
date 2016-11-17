Wysiwyg installation with CKEditor
#####################################

Follow this steps for installation of Wysiwyg files with CKEditor.

Dependencies
==============

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
====================

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

   STATIC_ROOT = os.path.join(BASE_DIR, 'media/')
   
   CKEDITOR_UPLOAD_PATH = "media/"
   
   CKEDITOR_CONFIGS = {
    'default': {
        'toolbar': 'Full',
        'height': 300,
        'width': '100%',
    },
    'basic': {
        'width': '100%',
        'toolbar': 'Basic',
        "toolbar_Basic": [['Source', '-', 'Save', 'NewPage', 'DocProps', 'Preview', 'Print', '-', 'Templates'],
                          ['Cut', 'Copy', 'Paste', 'PasteText', 'PasteFromWord', '-', 'Undo', 'Redo'],
                          ['Find', 'Replace', '-', 'SelectAll', '-', 'SpellChecker', 'Scayt'],
                          ['Form', 'Checkbox', 'Radio', 'TextField', 'Textarea', 'Select', 'Button', 'ImageButton',
                           'HiddenField'],
                          ['Bold', 'Italic', 'Underline', 'Strike', 'Subscript', 'Superscript', '-', 'RemoveFormat'],
                          ['NumberedList', 'BulletedList', '-', 'Outdent', 'Indent', '-', 'Blockquote', 'CreateDiv',
                           '-', 'JustifyLeft', 'JustifyCenter', 'JustifyRight', 'JustifyBlock', '-', 'BidiLtr',
                           'BidiRtl'],
                          ['Link', 'Unlink', 'Anchor'],
                          ['Table', 'HorizontalRule', 'Smiley', 'SpecialChar', 'PageBreak'],
                          ['Styles', 'Format', 'Font', 'FontSize'],
                          ['TextColor', 'BGColor'],
                          ['Maximize', 'ShowBlocks', '-', 'About']],
        "language": "en",
        "skin": "moono",
    },
    'empty': {
        'toolbar': 'Basic',
        'height': 200,
        'width': 500,
        "toolbar_Basic": [],
        "language": "en",
        "skin": "moono",
    }
}

* Install the collecstatic management command: Via pip.

.. code-block:: bash

    ./manage.py collectstatic


Code
=======

* You need to define a HTML template ("example_wysiwyg.html"). 

.. code-block:: bash

    {% load wysiwyg %}
    {% wysiwyg_setup %}

	<textarea id="foo"></textarea>

    {% wysiwyg_editor "foo" %}
