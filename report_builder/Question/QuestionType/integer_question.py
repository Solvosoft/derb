'''
Created on 14/9/2016

@author: natalia
'''
from report_builder.Question.QuestionView import QuestionViewAdmin, QuestionViewResp, QuestionViewPDF
from django.shortcuts import render
from report_builder.Question.forms import IntegerQuestionForm, AnswerForm
from report_builder.shortcuts import get_children
import random
from django.contrib import messages



class IntegerQuestionAdmin(QuestionViewAdmin):
    form_class=  IntegerQuestionForm
    template_name = 'admin/integer_question.html'
    name = 'integer_question'
    minimal_representation = {
        'human_readable_name': 'Numerical question',
        'help': 'Allows you to make inumerical questions',
        'color': '#330065'
    }
    
    def pre_save(self, object, request, form):
        children = get_children(form)
        object.answer_options = repr({'children': children})
        return object
    
    def additional_template_parameters(self, **kwargs):
        parameters = self.get_question_answer_options()
        if not parameters:
            parameters = {}
        parameters['children'] = self.process_children(self.request, parameters, kwargs)
        return parameters
    
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


class IntegerQuestionResp(QuestionViewResp):
    form_class = AnswerForm
    def get(self, request, *args, **kwargs):
        form = self.get_form(instance=self.question)
        print(form)
        parameters = {
            'form': form,
         }
        return render(request, 'responsable/integer_question.html',parameters)
        
