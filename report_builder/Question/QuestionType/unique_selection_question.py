'''
Created on 14/9/2016

@author: adolfo
'''
import json
import random

from django.http import Http404
from django.shortcuts import render
from django.contrib import messages
from report_builder.Question import QuestionView
from report_builder.Question.forms import UniqueSelectionAdminForm
from django_ajax.decorators import ajax

from report_builder.models import Question, Report
from report_builder.registry import models

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
        self.request = request
        self.form_number = random.randint(self.start_number, self.end_number)
        form = self.get_form(request.POST, instance=self.question)
        if form.is_valid():
            answer_options = {
                'catalog': int(form.cleaned_data.get('catalog')),
                'display_fields': form.cleaned_data.get('display_fields')
            }
            question = form.save(False)
            question.class_to_load = self.name
            question.report = Report.objects.first()
            question.answer_options = json.dumps(answer_options)
            question.save()
            messages.add_message(request, messages.SUCCESS, 'Question created successfully')
        else:
            messages.add_message(request, messages.ERROR, 'An error ocurred while creating the question')
        return self.get(request, *args, **kwargs)
       
class UniqueSelectionResp(QuestionView.QuestionViewResp):
    template_name = 'responsable/unique_selection_question.html'
    name = 'unique_selection_question'
    #form_class = BooleanAnswerForm

    def get(self, request, *args, **kwargs):
        """
            TODO: docstring
        """
        self.request = request
        self.form_number = random.randint(self.start_number, self.end_number)
        self.question = Question.objects.get(pk=kwargs['question_pk'])
        form = self.get_form(instance=self.answer)

        parameters = {
            'name': self.name,
            'form': form,
            'question': self.question,
            'question_number': self.question.order,
            'answer': self.answer,
            'form_number': str(self.form_number)
        }
        return render(request, self.template_name, parameters)
        
class UniqueSelectionPDF(QuestionView.QuestionViewPDF):
    def get(self, request, *args, **kwargs):
        return render(request, 'pdf/unique_selection_question.html')

@ajax
def get_catalog_display_fields(request):
    if request.method == 'GET':
        if request.is_ajax():
            catalog_id = int(request.GET.get('catalog_id', False))
            if catalog_id >= 0:
                catalog = models[catalog_id]
                return catalog[3]
    return 0
