'''
Created on 14/9/2016

@author: adolfo
'''
import json
import random

from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.contrib import messages
from django_ajax.decorators import ajax
from django.template import Context
from django.template.loader import get_template
from django.utils import timezone
from weasyprint import HTML

from report_builder.Question import QuestionView
from report_builder.Question.forms import UniqueSelectionAdminForm, \
    UniqueSelectionAnswerForm
from report_builder.models import Question, Answer, Report, ReportByProject
from report_builder.registry import models


class GetCatalogChoices():
    def get_catalog_choices(self, json_field):
        answer_options = json.loads(json_field)
        catalog = answer_options['catalog']
        display_field = answer_options['display_fields']

        list_fields = models[catalog][0]
        list_temp = []

        for object in list_fields:
            text = ""
            value = object.pk
            for i, field in enumerate(display_field):
                text += getattr(object, field)
                if (i + 1) != len(display_field):
                    text += ' - '
            list_temp.append((value, text))

        return tuple(list_temp)


class UniqueSelectionAdmin(QuestionView.QuestionViewAdmin):
    form_class = UniqueSelectionAdminForm
    template_name = 'admin/unique_selection_question.html'
    name = 'unique_selection_question'
    minimal_representation = {
        'human_readable_name': 'Unique Selection Question',
        'help': 'Allows you to make unique selection questions',
        'color': '#330065'
    }

    def get(self, request, *args, **kwargs):
        self.form_number = random.randint(self.start_number, self.end_number)
        self.request = request
        form = self.get_form(instance=self.question)
        parameters = {
            'form': form,
            'question': self.question,
            'name': self.name,
            'form_number': str(self.form_number),
            'minimal_representation': self.minimal_representation
        }
        return render(request, self.template_name, parameters)

    def post(self, request, *args, **kwargs):
        data = dict(request.POST)
        display_fields = data['display_fields']
        self.request = request
        self.form_number = random.randint(self.start_number, self.end_number)
        form = self.get_form(request.POST, instance=self.question)
        if form.is_valid():
            answer_options = {
                'catalog': int(form.cleaned_data.get('catalog')),
                'display_fields': display_fields
            }
            question = form.save(False)
            question.class_to_load = self.name
            question.report = Report.objects.first()
            question.answer_options = json.dumps(answer_options)
            question.save()
            messages.add_message(request, messages.SUCCESS, 'Question created successfully')
        else:
            print(form.errors)
            messages.add_message(request, messages.ERROR, 'An error ocurred while creating the question')
        return self.get(request, *args, **kwargs)


class UniqueSelectionResp(GetCatalogChoices, QuestionView.QuestionViewResp):
    template_name = 'responsable/unique_selection_question.html'
    name = 'unique_selection_question'
    form_class = UniqueSelectionAnswerForm

    def get(self, request, *args, **kwargs):
        """
            TODO: docstring
        """
        self.request = request
        self.form_number = random.randint(self.start_number, self.end_number)
        self.question = get_object_or_404(Question, pk=kwargs['question_pk'])
        json_field = self.question.answer_options

        catalog_choices = self.get_catalog_choices(json_field)

        form = self.get_form(instance=self.answer, extra=catalog_choices)

        parameters = {
            'name': self.name,
            'form': form,
            'question': self.question,
            'question_number': self.question.order,
            'answer': self.answer,
            'form_number': str(self.form_number)
        }
        return render(request, self.template_name, parameters)

    def post(self, request, *args, **kwargs):
        """
            TODO: docstring
        """
        self.request = request
        self.form_number = random.randint(self.start_number, self.end_number)
        self.question = get_object_or_404(Question, pk=kwargs['question_pk'])
        catalog_choices = self.get_catalog_choices(self.question.answer_options)

        if self.answer is None:
            self.answer = Answer()
        self.answer.question = self.question
        self.answer.user = request.user
        self.answer.text = ''
        self.answer.display_text = '\n'

        form = self.get_form(request.POST, instance=self.answer, extra=catalog_choices)

        if form.is_valid():
            answer = form.save(False)
            answer.question = self.question
            answer.user = request.user
            answer.report = ReportByProject.objects.first()
            self.answer = answer
            self.save(answer)
            messages.add_message(request, messages.SUCCESS, 'Question answered successfully')
        else:
            messages.add_message(request, messages.ERROR, 'An error ocurred while answering the question')

        return self.get(request, *args, **kwargs)


class UniqueSelectionPDF(GetCatalogChoices, QuestionView.QuestionViewPDF):
    name = 'unique_selection_question'
    template_name = 'pdf/unique_selection_question.html'

    def get(self, request, *args, **kwargs):
        self.request = request
        self.question = Question.objects.get(pk=kwargs['question_pk'])
        self.answer = Answer.objects.filter(question=self.question).first()
        json_field = self.question.answer_options
        catalog_choices = self.get_catalog_choices(json_field)
        userAnswer = ""
        if self.answer:
            userAnswer = catalog_choices[int(self.answer.text)][1]

        parameters = {
            'name': self.name,
            'question': self.question,
            'question_number': self.question.order,
            'answer': self.answer,
            'request': self.request,
            'form_number': str(random.randint(self.start_number, self.end_number)),
            'datetime': timezone.now(),
            'userAnswer': userAnswer
        }

        template = get_template(self.template_name)

        html = template.render(Context(parameters)).encode('UTF-8')

        page = HTML(string=html, encoding='utf-8').write_pdf()

        response = HttpResponse(page, content_type='application/pdf')

        response[
            'Content-Disposition'] = 'attachment; filename="question_report.pdf"'

        return response


@ajax
def get_catalog_display_fields(request):
    if request.method == 'GET':
        if request.is_ajax():
            catalog_id = request.GET.get('catalog_id', False)
            if catalog_id.isdigit():
                catalog_id = int(catalog_id)
                if catalog_id >= 0 and catalog_id < len(models):
                    catalog = models[catalog_id]
                    return catalog[3]
    return ()
