import random

from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import render

from report_builder.Question.QuestionView import QuestionViewAdmin
from report_builder.Question.QuestionView import QuestionViewResp
from report_builder.Question.QuestionView import QuestionViewPDF
from report_builder.Question.forms import BooleanAnswerForm
from report_builder.models import Question, Answer


class BooleanQuestionViewAdmin(QuestionViewAdmin):
    template_name = 'admin/boolean_question.html'
    name = 'boolean_question'
    minimal_representation = {
        'human_readable_name': 'Yes/No question',
        'help': 'Allows you to make yes/no questions',
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


class BooleanQuestionViewResp(QuestionViewResp):
    template_name = 'responsable/boolean_question.html'
    name = 'boolean_question'
    form_class = BooleanAnswerForm

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

    def post(self, request, *args, **kwargs):
        """
            TODO: docstring
        """
        self.request = request
        self.form_number = random.randint(self.start_number, self.end_number)
        self.question = Question.objects.get(pk=kwargs['question_pk'])

        if self.answer is None:
            self.answer = Answer()
        self.answer.question = self.question
        self.answer.user = request.user
        self.answer.text = ''
        self.answer.display_text = '\n'

        form = self.get_form(request.POST, instance=self.answer)
        if form.is_valid():
            answer = form.save(False)
            answer.question = self.question
            answer.user = request.user
            answer.report_id = 1
            self.answer = answer
            self.save(answer)
            messages.add_message(request, messages.SUCCESS, 'Question answered successfully')
        else:
            messages.add_message(request, messages.ERROR, 'An error ocurred while answering the question')

        return self.get(request, *args, **kwargs)


class BooleanQuestionViewPDF(QuestionViewPDF):
    pass
