import csv
import json
import random
import reversion

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import transaction
from django.utils import timezone
from django.http import HttpResponse
from django.template.loader import get_template
from django.shortcuts import render, get_object_or_404, redirect
from django.views.defaults import bad_request
from django.views.generic.base import View
from django.utils.datastructures import OrderedDict
from django.template import Context
from weasyprint import HTML
from io import StringIO
#from savReaderWriter import SavWriter
from tempfile import NamedTemporaryFile
from django.conf import settings
from report_builder.Observation.ObservationView import ObservationView
from report_builder.Question.question_loader import process_questions
from report_builder.models import Question as QuestionModel, Answer, Report, ReportByProject
from report_builder.Question.forms import QuestionForm, AnswerForm, ObservationForm
from report_builder.report_shortcuts import get_question_permission
from report_builder.shortcuts import transform_request_to_get, get_children, get_reportbyproj_question_answer
from report_builder.Question import question_loader


class Question(LoginRequiredMixin, View):
    """
        Question class contains the general functionality for a question object, and sets the base for the different
        question types of the Derb system.

        Until now, this are the question types that can be created based on Question:

            - simple_text_question
            - boolean_question
            - integer_question
            - float_question
            - unique_selection_question

        The Question class also provides the way to extend the functionality of a question object. For instance:

            * Define additional answer options to the question object
            * Define additional context attributes to the question template
            * Modify question form parameters
    """
    template_name = 'admin/base_question.html'  #: Specifies which template to load
    form_class = QuestionForm  #: Default form for the class
    base_model = QuestionModel  #: Base model for the form (:mod:`report_builder.models.Question`)
    name = 'simple_question'  #: Class reference name
    question = None  #: Question instance
    answer = None  #: Answer reference (if it exists)
    start_number = 500  #: Random start value for the question template
    end_number = 10000  #: Random end value  for the question template
    form_number = 0  #: Unique value for the view
    view_type = 'admin'  #: View type to load, it can be: admin, responsable, revisor, pdf, csv, json
    request = None  #: Copy of the request provided by the view (GET or POST)

    def get_question_answer_options(self):
        """
            Returns a dict with extra options for the question. It uses JSON parsing to unpack the answer options
        """
        results = None
        if self.question is not None and self.question.answer_options:
            results = json.loads(self.question.answer_options)
        return results

    def additional_template_parameters(self, **kwargs):
        """
            Allows to add extra entries to the template context.
            It receives a copy of the context and must return only the extra parameters (answer_options)

            .. note:: This method is called before the templated is rendered
        """
        return self.get_question_answer_options()

    def pre_save(self, object, request, form):
        """
            It allows add or set attributes to the question object.
            The data can be extracted directly from the request (POST) or the form provided.
            It returns the instance of the object with the modifications applied
        """
        return object

    def get_form(self, post=None, instance=None, extra=None):
        """
            It allows to add or set attributes to the question form.
            *extra* is a a dictionary tha is passed to the form constructor
            If you want to override this method in a class that extends from Question, you have to do it like this:

            .. code:: python

                class ExampleClass(Question):

                    def get_form(self, post=None, instance=None, extra=None):
                        extra = {
                            'extra_value': data
                        }
                        return super(ExampleClass, self).get_form(post=post, instance=instance, extra=extra)
        """
        form = None
        if extra is None:
            form = self.form_class(instance=instance)
            if post is not None:
                form = self.form_class(post, instance=instance)
        else:
            form = self.form_class(instance=instance, extra=extra)
            if post is not None:
                form = self.form_class(post, instance=instance, extra=extra)
        return form

    def get_observations(self, request, *args, **kwargs):
        '''
            Returns the observations rendered template for the question object (to allow to see, allow and add observations)
        '''
        request = transform_request_to_get(request=request)
        observation_view = ObservationView.as_view()
        keywords = self.kwargs
        if self.answer:
            keywords['answer_pk'] = self.answer.pk
        else:
            keywords['answer_pk'] = None
        observations = observation_view(request, *args, **keywords)
        return observations.render().content

    def process_children(self, request, parameters, arguments, include=None):
        """
            Allows to process the children questions for the current question
        """
        if include is None:
            include = []
        children = {}
        report = arguments['report']
        children_parameters = {}

        if 'children' in parameters and parameters['children'] is not None:
            children_parameters = OrderedDict(parameters['children'])
            for child, value in children_parameters.items():
                if not include or child in include:
                    children[child] = {
                        'state': 'ok',
                        'text': question_loader.process_questions(request, report.report.pk, value,
                                                                  view_type=self.view_type, reportbyproj=report)
                    }


class QuestionViewAdmin(Question):
    '''
        QuestionViewAdmin class represents the implementation of the template administrator view for a question object
        This view is built to be extended from the different question types of the Derb system
        By itself, this view provides the functionality for ordering and deletion of question, and a form with question
        text and help

        This class be extended using an implementation like this:

        .. code:: python

            from report_builder.Question.QuestionView import QuestionViewAdmin
            class MyQuestion(QuestionViewAdmin):
                template_name = 'path/to/the/template'
                name = 'my_question'

        The extended methods can be overridden to adjust the functionality of the extended class. For instance:

        .. code:: python

            def additional_template_parameters(self, **kwargs):
                some_dict = {
                    'something': some_variable
                }
                return some_dict

        .. note::
            *kwargs* is a dict that contains the Question attributes 'form', 'report', 'question' and 'name'
            You don't have to append the kwargs content in the return value, only the additional elements
    '''
    template_name = 'admin/base_question.html'
    name = 'simple_question'
    request = None
    minimal_representation = {
        'human_readable_name': 'Simple question',
        'help': 'Allows to create text questions where the user can answer whatever it wants',
        'color': '#003768'
    }

    def get(self, request, *args, **kwargs):
        '''
            Handles the requests using the *GET* HTTP verb triggered by the template administrator
            The context passed to the template contains (at least) the next elements:
                - form
                - report
                - question
                - name
                - form_number
                - minimal_representation
            Returns the rendered template for the question
        '''
        question_pk = kwargs.get('question_pk', False)
        report_pk = kwargs.get('report_pk', False)

        if question_pk and question_pk != '':
            self.question = get_object_or_404(QuestionModel, pk=question_pk)
            question_pk = self.question.pk
        else:
            question_pk = ''

        self.report = get_object_or_404(Report, pk=report_pk)

        self.form_number = random.randint(self.start_number, self.end_number)
        self.request = request
        form = self.get_form(instance=self.question)
        parameters = {
            'form': form,
            'question': self.question,
            'report': self.report,
            'name': self.name,
            'form_number': str(self.form_number),
            'minimal_representation': self.minimal_representation,
            'question_pk': question_pk
        }
        extra = self.additional_template_parameters(**parameters)
        if extra:
            parameters.update(extra)
        return render(request, self.template_name, parameters)

    def post(self, request, *args, **kwargs):
        '''
            Handles the requests using the *POST* HTTP verb triggered by the template administrator
            The context passed to the template contains (at least) the next elements:
                - form
                - report
                - question
                - name
                - form_number
                - minimal_representation
            Returns the question pk when the POST request is processed correctly
            Return the rendered template (with errors) when the form presents errors
        '''
        question_pk = kwargs.get('question_pk', False)
        report_pk = kwargs.get('report_pk', False)

        if question_pk and question_pk != '':
            self.question = get_object_or_404(QuestionModel, pk=question_pk)
            redirection_needed = False

        if report_pk and report_pk != '':
            self.report = get_object_or_404(Report, pk=report_pk)

        self.request = request
        self.form_number = random.randint(self.start_number, self.end_number)
        form = self.get_form(request.POST, instance=self.question)

        if form.is_valid():
            question = form.save(False)
            question.class_to_load = self.name
            question.report = self.report
            question = self.pre_save(question, request, form)
            question.save()
            messages.add_message(request, messages.SUCCESS, 'Question saved successfully')

            return HttpResponse(question.pk, status=200)
        else:
            messages.add_message(request, messages.ERROR, 'An error ocurred while creating the question')

        parameters = {
            'form': form,
            'report': self.report,
            'question': self.question,
            'name': self.name,
            'form_number': str(self.form_number),
            'minimal_representation': self.minimal_representation,
            'question_pk': question_pk
        }
        extra = self.additional_template_parameters(**parameters)
        if extra:
            parameters.update(extra)

        return render(request, template_name=self.template_name, context=parameters, status=302)

    def process_children(self, request, parameters, arguments, include=None):
        '''
            Gets the rendered template (HTML code) for every child question of the current question

            :param request:
            :param dict parameters: context parameters passed to the template, generally self.question.answer_options
            :param dict arguments: parameters passed to the function additional_template_parameters
            :return: list of string with the rendered templates for the child questions
        '''

        if include is None:
            include = []
        return_value = {}
        report = arguments['report']
        form = arguments['form']
        children = get_children(form)
        if children is None and parameters and 'children' in parameters and parameters['children']:
            children = parameters['children']
        if children:
            for child in children:
                return_value[child] = process_questions(request, report.pk, children[child], view_type=self.view_type)
        return return_value


class QuestionViewResp(Question):
    """
        QuestionViewResp class represents the implementation of the template administrator view for a question object
        This view is built to be extended from the different question types of the Derb system
        By itself, this view shows the simple question created by the template administrator, including the question text and help
        set by the user. Additionally, it provides a form two fields, a text area for the user to answer the question and a text area
        to add annotations for the reviewers. Plus, when a reviewer user has applied observations to the question, it shows such observations.

        .. note::
            * Extends from the Question class, so if you want to take a look to the extended methods and attributes,
            you can find it in :mod:`report_builder.Question.QuestionView.Question`
    """
    template_name = 'responsable/simple_question.html'
    form_class = AnswerForm
    name = 'simple_question'
    answer = None
    registry_type = 'select'
    view_type = 'responsable'

    def get(self, request, *args, **kwargs):
        '''
             Handles the requests using the *GET* HTTP verb triggered by the responsable
             The context passed to the template contains (at least) the next elements:
                - name
                - form
                - question
                - question_number
                - answer
                - reportbyproj
                - form_number
                - observations
                - requirement
        '''
        self.request = request
        self.form_number = random.randint(self.start_number, self.end_number)
        self.question = get_object_or_404(QuestionModel, pk=kwargs['question_pk'])
        reportbyproj = get_object_or_404(ReportByProject, pk=kwargs['report_pk'])

        if Answer.objects.filter(report=reportbyproj, question=self.question).exists():
            self.answer = Answer.objects.get(report=reportbyproj, question=self.question)

        form = self.get_form(instance=self.answer)

        parameters = {
            'name': self.name,
            'form': form,
            'question': self.question,
            'question_number': self.question.order,
            'answer': self.answer,
            'reportbyproj': reportbyproj,
            'form_number': str(self.form_number)
        }
        extra = self.additional_template_parameters(**parameters)
        if extra:
            parameters.update(extra)

        return render(request, self.template_name, parameters)

    def post(self, request, *args, **kwargs):
        '''
            Handles the requests using the *POST* HTTP verb triggered by the responsable
            The context passed to the template contains (at least) the next elements:
               - name
               - form
               - question
               - question_number
               - answer
               - reportbyproj
               - form_number
               - observations
               - requirement
            Returns the answer pk when the POST request is processed correctly
            Return the rendered template (with errors) when the form presents errors
       '''
        self.request = request
        self.form_number = random.randint(self.start_number, self.end_number)
        self.question = get_object_or_404(QuestionModel, pk=kwargs['question_pk'])
        reportbyproj = get_object_or_404(ReportByProject, pk=kwargs['report_pk'])
        if Answer.objects.filter(report=reportbyproj, question=self.question).exists():
            self.answer = Answer.objects.get(report=reportbyproj, question=self.question)

        if self.answer is None:
            self.answer = Answer()
        self.answer.question = self.question
        self.answer.user = request.user

        self.answer.text = ''
        self.answer.display_text = '\n'

        form = self.get_form(post=request.POST, instance=self.answer)

        if form.is_valid():
            answer = form.save(False)
            answer.report = reportbyproj
            answer.question = self.question
            answer.user = request.user
            self.answer = answer
            self.save(answer)
            return HttpResponse(str(answer.pk))

        parameters = {
            'name': self.name,
            'form': form,
            'question': self.question,
            'reportbyproj': reportbyproj,
            'question_number': self.question.order,
            'answer': self.answer,
            'form_number': str(self.form_number),
            # 'observations': self.get_observations(request, args, kwargs),
            'required': get_question_permission(self.question)
        }
        extra = self.additional_template_parameters(**parameters)
        if extra:
            parameters.update(extra)
        return render(request, self.template_name, parameters)

    def save(self, klass):
        with transaction.atomic(), reversion.create_revision():
            klass.save()
            reversion.set_user(self.request.user)

    def is_valid_question(self, reportbyproj_pk, question_pk, answer_pk):
        '''
            Checks if the question has been answered correctly
            Used when checking if the report is complete before to submit for revision or when the user request the report status

            In the case that the question has not been answered correctly or answered at all, returns the error info
        '''
        question = None
        try:
            question = QuestionModel.objects.get(pk=question_pk)
        except:
            return [
                {
                    'pk': question_pk,
                    'number': 'Undefined',
                    'problem': 'Question object doesn\'t exist'
                }
            ]

        permission = get_question_permission(question)
        if permission == 1:
            if answer_pk is not None:
                try:
                    answer = Answer.objects.get(pk=answer_pk)
                    if not answer.text:
                        return [
                            {
                                'pk': question_pk,
                                'number': question.order,
                                'problem': 'Blank answer'
                            }
                        ]
                except:
                    return [
                        {
                            'pk': question_pk,
                            'number': question.order,
                            'problem': 'No answer'
                        }
                    ]
            else:
                return [
                    {
                        'pk': question_pk,
                        'number': question.order,
                        'problem': 'No answer'
                    }
                ]


class QuestionViewPDF(Question):
    """
        QuestionViewPDF class represents the implementation of exporting a question object to a PDF document
        This view is built to be extended from the different question types of the Derb system
        By itself, this view saves in the PDF the simple question created by the template administrator, including
        the question text and help set by the user. Additionally, if a responsable user has answered the question,
        it shows the answer text and annotations provided. Finally, if one or more reviewer users applied
        observations to the question, it shows such observations.

        .. note::
            * Extends from the Question class, so if you want to take a look to the extended methods and attributes,
            you can find it in :mod:`report_builder.Question.QuestionView.Question`
    """
    template_name = "pdf/simple_question.html"
    form_class = None
    name = 'simple_question'
    view_type = 'pdf'
    answer = None
    registry_type = 'select'

    def post(self, request, *args, **kwargs):
        """
            This view can be handled only using the GET verb
            For security reasons, when a request is sent using the POST verb, the 403 exception is raised
        """
        return bad_request(request)

    def get(self, request, *args, **kwargs):
        """
             Handles the requests using the *GET* HTTP verb triggered by a user to export a question to a PDF document
             The context passed to the template contains (at least) the next elements:
                - name
                - form
                - question
                - question_number
                - answer
                - reportbyproj
                - form_number
                - observations
                - requirement
        """
        self.request = request
        self.form_number = random.randint(self.start_number, self.end_number)
        self.question = get_object_or_404(QuestionModel, pk=kwargs['question_pk'])
        reportbyproj = get_object_or_404(ReportByProject, pk=kwargs['report_pk'])
        if Answer.objects.filter(report=reportbyproj, question=self.question).exists():
            self.answer = Answer.objects.get(report=reportbyproj, question=self.question)

        parameters = {
            'name': self.name,
            'question': self.question,
            'question_number': self.question.order,
            'answer': self.answer,
            'form_number': str(random.randint(self.start_number, self.end_number)),
            'datetime': timezone.now(),
        }
        additional = self.additional_template_parameters(**parameters)
        if additional:
            parameters.update(additional)
        template = get_template(self.template_name)

        html = template.render(Context(parameters)).encode('UTF-8')

        page = HTML(string=html, encoding='utf-8').write_pdf()

        response = HttpResponse(page, content_type='application/pdf')

        response[
            'Content-Disposition'] = 'attachment; filename="question_report.pdf"'

        return response


class QuestionViewReviewer(Question):
    """
        QuestionViewReviewer class represents the implementation of the reviewer view for a question object
        This view is built to be extended from the different question types of the Derb system
        By itself, this view shows the simple question created by the template administrator, including
        the question text and help set by the user. Additionally, if a responsable user has answered the question,
        it shows the answer text and annotations provided. Finally, if one or more reviewer users applied
        observations to the question, it shows such observations.

        .. note::
            * Extends from the Question class, so if you want to take a look to the extended methods and attributes,
            you can find it in :mod:`report_builder.Question.QuestionView.Question`
    """
    template_name = 'reviewer/simple_question.html'
    view_type = 'reviewer'
    answer = None
    name = 'simple_question'
    form_class = ObservationForm

    def post(self, request, *args, **kwargs):
        return bad_request(request)

    def get(self, request, *args, **kwargs):
        self.request = request
        self.form_number = random.randint(self.start_number, self.end_number)
        self.question = get_object_or_404(QuestionModel, pk=kwargs['question_pk'])
        reportbyproj = get_object_or_404(ReportByProject, pk=kwargs['report_pk'])
        if Answer.objects.filter(report=reportbyproj, question=self.question).exists():
            self.answer = Answer.objects.get(report=reportbyproj, question=self.question)

        form = self.get_form()

        parameters = {
            'name': self.name,
            'question': self.question,
            'question_number': self.question.order,
            'answer': self.answer,
            'form': form,
            'form_number': str(random.randint(self.start_number, self.end_number)),
        }

        return render(request, self.template_name, parameters)


class QuestionViewCSV(Question):
    """
        QuestionViewJSON class represents the implementation of exporting a question object to a CSV formatted string
        This view is built to be extended from the different question types of the Derb system
        By itself, this view saves in the CSV string the simple question created by the template administrator, including
        the question text and help set by the user. Additionally, if a responsable user has answered the question,
        it saves the answer text and annotations provided. Finally, if one or more reviewer users applied
        observations to the question, it saves such observations.

        .. note::
            * Extends from the Question class, so if you want to take a look to the extended methods and attributes,
            you can find it in :mod:`report_builder.Question.QuestionView.Question`
    """
    name = 'simple_question'
    view_type = 'csv'
    answer = None

    def get_question_data(self, question, report, answer=None):
        """
            Recovers the question data, according to its definition and related objects (report, answer, observations)
        """
        data = {}

        data['pk'] = question.pk
        data['report'] = report.pk
        data['text'] = question.text
        data['help'] = question.help
        data['required'] = question.required
        data['order'] = question.order

        if answer is not None:
            data['answer_pk'] = answer.pk
            data['answer_text'] = answer.text
            data['answer_annotation'] = answer.annotation
            data['answer_display_text'] = answer.display_text
        else:
            data['answer_pk'] = ''
            data['answer_text'] = ''
            data['answer_annotation'] = ''
            data['answer_display_text'] = ''

        return data

    def get(self, request, *args, **kwargs):
        """
            Handles the requests using the *GET* HTTP verb triggered by a user to export a question to a CSV string
            The context passed to the template contains (at least) the next elements:
               - name
               - form
               - question
               - question_number
               - answer
               - reportbyproj
               - form_number
               - observations
               - requirement
       """
        self.request = request
        self.form_number = random.randint(self.start_number, self.end_number)
        self.question = get_object_or_404(QuestionModel, pk=kwargs['question_pk'])
        reportbyproj = get_object_or_404(ReportByProject, pk=kwargs['report_pk'])
        if Answer.objects.filter(report=reportbyproj, question=self.question).exists():
            self.answer = Answer.objects.get(report=reportbyproj, question=self.question)

        data = self.get_question_data(self.question, reportbyproj, self.answer)

        csv_output = StringIO()

        csv_writer = csv.writer(csv_output)
        csv_writer.writerow(list(data.values()))

        return HttpResponse(csv_output.getvalue())

    def post(self, request, *args, **kwargs):
        """
            This view can be handled only using the GET verb
            For security reasons, when a request is sent using the POST verb, the 403 exception is raised
        """
        return bad_request(request)


class QuestionViewJSON(Question):
    """
        QuestionViewJSON class represents the implementation of exporting a question object to a JSON formatted string
        This view is built to be extended from the different question types of the Derb system
        By itself, this view saves in the JSON string the simple question created by the template administrator, including
        the question text and help set by the user. Additionally, if a responsable user has answered the question,
        it saves the answer text and annotations provided. Finally, if one or more reviewer users applied
        observations to the question, it saves such observations.

        .. note::
            * Extends from the Question class, so if you want to take a look to the extended methods and attributes,
            you can find it in :mod:`report_builder.Question.QuestionView.Question`
    """
    name = 'simple_question'
    view_type = 'json'
    answer = None

    def get_question_data(self, question, report, answer=None):
        """
            Recovers the question data, according to its definition and related objects (report, answer, observations)
        """
        data = {}

        data['pk'] = question.pk
        data['report'] = report.pk
        data['text'] = question.text
        data['help'] = question.help
        data['required'] = question.required
        data['order'] = question.order

        if answer is not None:
            data['answer'] = {
                'pk': answer.pk,
                'text': answer.text,
                'annotation': answer.annotation,
                'display_text': answer.display_text
            }

        return data

    def get(self, request, *args, **kwargs):
        '''
            Handles the requests using the *GET* HTTP verb triggered by a user to export a question to a PDF document
            The context passed to the template contains (at least) the next elements:
               - name
               - form
               - question
               - question_number
               - answer
               - reportbyproj
               - form_number
               - observations
               - requirement
       '''
        self.request = request
        self.form_number = random.randint(self.start_number, self.end_number)
        self.question = get_object_or_404(QuestionModel, pk=kwargs['question_pk'])
        reportbyproj = get_object_or_404(ReportByProject, pk=kwargs['report_pk'])
        if Answer.objects.filter(report=reportbyproj, question=self.question).exists():
            self.answer = Answer.objects.get(report=reportbyproj, question=self.question)

        data = self.get_question_data(self.question, reportbyproj, self.answer)

        json_data = json.dumps(data)

        return HttpResponse(json_data)

    def post(self, request, *args, **kwargs):
        """
            This view can be handled only using the GET verb
            For security reasons, when a request is sent using the POST verb, the 403 exception is raised
        """
        return bad_request(request)


class QuestionViewSPSS(Question):
    name = 'simple_question'
    view_type = 'spss'
    answer = None

    def get_question_data(self, question, report, answer=None):
        varNames = [
            'pk',
            'report_pk',
            'text',
            'help',
            'required',
            'order',
            'answer_pk',
            'answer_text',
            'answer_annotation',
            'answer_display_text'
        ]

        varTypes = {
            'pk': 0,
            'report_pk': 0,
            'text': 255,
            'help': 255,
            'required': 0,
            'order': 0,
            'answer_pk': 0,
            'answer_text': 255,
            'answer_annotation': 255,
            'answer_display_text': 255
        }

        record = []

        record = record + [question.pk, report.pk, question.text, question.help, question.required,
                           question.order]
        if answer:
            record = record + [answer.pk, answer.text, answer.annotation, answer.display_text]
        else:
            record = record + ['', '', '', '']

        return varNames, varTypes, record

    def get(self, request, *args, **kwargs):
        self.request = request
        self.form_number = random.randint(self.start_number, self.end_number)
        self.question = get_object_or_404(QuestionModel, pk=kwargs['question_pk'])
        reportbyproj = get_object_or_404(ReportByProject, pk=kwargs['report_pk'])
        if Answer.objects.filter(report=reportbyproj, question=self.question).exists():
            self.answer = Answer.objects.get(report=reportbyproj, question=self.question)

        varNames, varTypes, record = self.get_question_data(self.question, reportbyproj, self.answer)

        spss_output = settings.MEDIA_ROOT + 'question.sav'

        #with SavWriter(spss_output, varNames, varTypes) as writer:
         #   writer.writerow(record)

        return HttpResponse(0)

    def post(self, request, *args, **kwargs):
        return bad_request(request)
