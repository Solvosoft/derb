'''
Created on 14/9/2016

@author: adolfo
'''
import random

from django.shortcuts import render
from django.contrib import messages

from report_builder.Question import QuestionView
from report_builder.Question.forms import UniqueSelectionForm

class UniqueSelectionAdmin(QuestionView.QuestionViewAdmin):
    form_class = UniqueSelectionForm
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
            question = form.save(False)
            question.class_to_load = self.name
            question.report_id = 1
            question.save()
            messages.add_message(request, messages.SUCCESS, 'Question created successfully')
        else:
            messages.add_message(request, messages.ERROR, 'An error ocurred while creating the question')
        return self.get(request, *args, **kwargs)
       
class UniqueSelectionResp(QuestionView.QuestionViewResp):
    def get(self, request, *args, **kwargs):
        return render(request, 'responsable/unique_selection_question.html')
        
class UniqueSelectionPDF(QuestionView.QuestionViewPDF):
    def get(self, request, *args, **kwargs):
        return render(request, 'pdf/unique_selection_question.html')
