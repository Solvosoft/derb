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


def get_catalog_values(queryset, display_fields):
    for object in queryset:
        text = ""
        value = object.pk
        for i, field in enumerate(display_fields):
            text += getattr(object, field)
            if (i + 1) != len(display_fields):
                text += ' - '
        yield (value, text)

def get_catalog_choices(json_field):
    answer_options = json.loads(json_field)
    catalog = int(answer_options['catalog'][0])
    display_fields = answer_options['display_fields']
    queryset = models[catalog][0]

    return (value_text for value_text in get_catalog_values(queryset, display_fields))



class UniqueSelectionAdmin(QuestionView.QuestionViewAdmin):
    form_class = UniqueSelectionAdminForm
    template_name = 'admin/unique_selection_question.html'
    name = 'unique_selection_question'
    minimal_representation = {
        'human_readable_name': 'Unique Selection Question',
        'help': 'Allows you to make unique selection questions',
        'color': '#330065'
    }

    def pre_save(self, object, request, form):
        form_data = dict(form.data)
        answer_options = {
            'catalog': form_data.get('catalog'),
            'display_fields': form_data.get('display_fields')
        }
        object.answer_options = json.dumps(answer_options)
        return object


class UniqueSelectionResp(QuestionView.QuestionViewResp):
    template_name = 'responsable/unique_selection_question.html'
    name = 'unique_selection_question'
    form_class = UniqueSelectionAnswerForm

    def get_form(self, post=None, instance=None, extra=None):
        catalog_choices = get_catalog_choices(self.question.answer_options)
        print(catalog_choices)
        form = self.form_class(instance=instance, extra=catalog_choices)
        return form

    '''
    def post(self, request, *args, **kwargs):
        """
            TODO: docstring
        """
        self.request = request
        self.form_number = random.randint(self.start_number, self.end_number)
        self.question = get_object_or_404(Question, pk=kwargs['question_pk'])
        catalog_choices = get_catalog_choices(self.question.answer_options)

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
    '''


class UniqueSelectionPDF(QuestionView.QuestionViewPDF):
    name = 'unique_selection_question'
    template_name = 'pdf/unique_selection_question.html'

    def get(self, request, *args, **kwargs):
        self.request = request
        self.question = Question.objects.get(pk=kwargs['question_pk'])
        self.answer = Answer.objects.filter(question=self.question).first()
        json_field = self.question.answer_options
        catalog_choices = get_catalog_choices(json_field)
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
