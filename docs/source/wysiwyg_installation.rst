Wysiwyg installation with CKEditor
##############################

Follow this steps for installation of Wysiwyg files with CKEditor.

Dependencies
============

* Install packages: Via pip, you must install your platform’s packages (Linux, Debian/Ubuntu).

.. code-block:: bash

    $ pip install django-wysiwyg

* Configuration: Add ‘django_wysiwyg’ to your INSTALLED_APPS in settings.py:

.. code-block:: bash

    INSTALLED_APPS = (
    ...
    'django_wysiwyg',
    )

.. code-block:: bash

    pip install --upgrade setuptools pip

* Finally, you going to install Weasyprint.

.. code-block:: bash

    pip install WeasyPrint

Code
====

* You need to define a HTML template ("example_pdf.html"). In this HTML template, you can define the top, the body and the bottom of the PDF file.

.. code-block:: bash

    <html>
        <head>
            <style>
                @page {
                    margin: 3cm 2cm; padding-left: 1.5cm;

                    @top-left {
                        content: "Example Report";
                    }
                    @top-right {
                        content: "Date: {{ datetime }}";
                    }
                    @bottom-right {
                        content: "Page " counter(page) " of " counter(pages) ;
                    }
                    @bottom-left {
                        content:  "User: {{ request.user }}";
                        color: red;
                    }
                }
                body {
                    text-align: justify
                }
            </style>
        </head>
        <body>
            <h3>
                Hello, this is my report!!
            </h3>
        </body>
    </html>

* Define the PDF generator method.

.. code-block:: python

    def report_example(request):
        varModel = Model.objects.all()

        template = get_template('pdf/example_pdf.html')

        context = {
                   'object_list': varModel,
                   'datetime': timezone.now(),
                   'request': request
                   }

        html = template.render(Context(context)).encode("UTF-8")

        page = HTML(string=html, encoding='utf-8').write_pdf()

        response = HttpResponse(page, content_type='application/pdf')

        response[
                  'Content-Disposition'] = 'attachment; filename="report_example.pdf"'
        return response

* Create the URL.

.. code-block:: python

    url(r"^report/example$", views.report_example, name="report_example"),
