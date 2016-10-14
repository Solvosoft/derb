import csv
import json
import random
import reversion

from django.contrib import messages
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
from report_builder.Observation.ObservationView import ObservationView
from report_builder.Question.question_loader import process_questions
from report_builder.models import Question as QuestionModel, Answer, Report, ReportByProject
from report_builder.Question.forms import QuestionForm, AnswerForm, ObservationForm
from report_builder.report_shortcuts import get_question_permission
from report_builder.shortcuts import transform_request_to_get, get_children, get_reportbyproj_question_answer
from report_builder.Question import question_loader


class Question(View):
    """
        TODO: docstring
    """
    # TODO: define template
    template_name = 'admin/simple_question.html'
    form_class = QuestionForm
    base_model = QuestionModel
    name = 'simple_question'
    question = None
    start_number = 500
    end_number = 10000
    report_number = 0
    view_type = 'admin'
    request = None

    def get_question_answer_options(self):
        """
            TODO: docstring
        """
        results = None
        if self.question is not None and self.question.answer_options:
            results = json.loads(self.question.answer_options)
        return results

    def additional_template_parameters(self, **kwargs):
        """
            TODO: docstring
        """
        return self.get_question_answer_options()

    def pre_save(self, object, request, form):
        """
            TODO: docstring
        """
        return object

    def get_form(self, post=None, instance=None, extra=None):
        """
            TODO: docstring
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
        """
            TODO: docstring
        """
        request = transform_request_to_get(request=request)
        observation_view = ObservationView.as_view()
        keywords = self.kwargs
        if self.answer:
            keywords['answer_pk'] = self.answer.pk
        else:
            keywords['answer_pk'] = None
        observations = observation_view(request, *args, **keywords)
        return observations.render().content

    def process_children(self, request, parameters, arguments, include=[]):
        """
            TODO: docstring
        """
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
    """
        TODO: docstring
    """
    template_name = 'admin/simple_question.html'
    name = 'simple_question'
    request = None
    minimal_representation = {
        'human_readable_name': 'Simple question',
        'help': 'Allows to create text questions where the user can answer whatever it wants',
        'color': '#003768'
    }

    def get(self, request, *args, **kwargs):
        """
            TODO: docstring
        """
        question_pk = kwargs.get('question_pk', False)
        report_pk = kwargs.get('report_pk', False)

        if question_pk and question_pk != '':
            self.question = get_object_or_404(QuestionModel, pk=question_pk)
            question_pk = self.question.pk

        if report_pk and report_pk != '':
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
        """
            TODO: docstring
        """
        redirection_needed = True
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
            question_pk = question.pk
            messages.add_message(request, messages.SUCCESS, 'Question saved successfully')

            if redirection_needed == True:
                return redirect(request.path + str(question_pk))
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
        return render(request, template_name=self.template_name, context=parameters)

    def process_children(self, request, parameters, arguments, include=[]):
        """
            TODO: docstring
        """
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
        TODO: docstring
    """
    template_name = 'responsable/simple_question.html'
    form_class = AnswerForm
    name = 'simple_question'
    answer = None
    registry_type = 'select'
    view_type = 'responsable'

    def get(self, request, *args, **kwargs):
        """
            TODO: docstring
        """
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
        """
            TODO: docstring
        """
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
        TODO: docstring
    """
    template_name = "pdf/simple_question.html"
    form_class = None
    name = 'simple_question'
    view_type = 'pdf'
    answer = None
    registry_type = 'select'

    def post(self, request, *args, **kwargs):
        """
            TODO: docstring
        """
        return bad_request(request)

    def get(self, request, *args, **kwargs):
        """
            TODO: docstring
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
        TODO: docstring
    """
    template_name = 'reviewer/simple_question.html'
    view_type = 'reviewer'
    answer = None
    name = 'simple_question'
    form_class = ObservationForm

    def post(self, request, *args, **kwargs):
        """
            TODO: docstring
        """
        return bad_request(request)

    def get(self, request, *args, **kwargs):
        """
            TODO: docstring
        """
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
    name = 'simple_question'
    view_type = 'csv'
    answer = None

    def get_question_data(self, question, report, answer=None):
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
        else:
            data['answer'] = ''

        return data

    def get(self, request, *args, **kwargs):
        self.request = request
        self.form_number = random.randint(self.start_number, self.end_number)
        self.question = get_object_or_404(QuestionModel, pk=kwargs['question_pk'])
        reportbyproj = get_object_or_404(ReportByProject, pk=kwargs['report_pk'])
        if Answer.objects.filter(report=reportbyproj, question=self.question).exists():
            self.answer = Answer.objects.get(report=reportbyproj, question=self.question)

        data = self.get_question_data(self.question, reportbyproj, self.answer)

        csv_output = StringIO()

        csv_writer = csv.writer(csv_output)
        csv_writer.writerow(list(data.keys()))
        csv_writer.writerow(list(data.values()))

        response = HttpResponse(csv_output.getvalue(), content_type='text/csv')

        response[
            'Content-Disposition'] = 'attachment; filename="question.csv"'
        return response

    def post(self, request, *args, **kwargs):
        return bad_request(request)


class QuestionViewJSON(Question):
    name = 'simple_question'
    view_type = 'json'
    answer = None

    def get_question_data(self, question, report, answer=None):
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
        else:
            data['answer'] = ''

    def get(self, request, *args, **kwargs):
        self.request = request
        self.form_number = random.randint(self.start_number, self.end_number)
        self.question = get_object_or_404(QuestionModel, pk=kwargs['question_pk'])
        reportbyproj = get_object_or_404(ReportByProject, pk=kwargs['report_pk'])
        if Answer.objects.filter(report=reportbyproj, question=self.question).exists():
            self.answer = Answer.objects.get(report=reportbyproj, question=self.question)

        data = self.get_question_data(self.question, reportbyproj, self.answer)

        json_data = json.dumps(data)

        response = HttpResponse(json_data, content_type='application/json')

        response[
            'Content-Disposition'] = 'attachment; filename="question.json"'
        return response

    def post(self, request, *args, **kwargs):
        return bad_request(request)


class QuestionViewSPSS(Question):
    pass
