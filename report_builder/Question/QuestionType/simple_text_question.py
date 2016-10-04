'''
Created on 15/9/2016

@author: nashyra
'''
import json
import random

from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import render
from django.template import Context
from django.template.loader import get_template
from django.utils import timezone
from weasyprint import HTML

from report_builder.Question.QuestionView import QuestionViewAdmin, QuestionViewResp, QuestionViewPDF
from report_builder.Question.forms import SimpleTextQuestionForm, SimpleTextAnswerForm
from report_builder.models import Question, Answer, Report, ReportByProject



class SimpleTextQuestionAdmin(QuestionViewAdmin):
    form_class = SimpleTextQuestionForm
    template_name = 'admin/simple_text_question.html'
    name = 'simple_text_question'
    minimal_representation = {
        'human_readable_name': 'Simple text question',
        'help': 'Allows you to make simple text questions',
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
            question.report = Report.objects.first()
            question.answer_options = json.dumps({})
            question.save()
            messages.add_message(request, messages.SUCCESS, 'Question created successfully')
        else:
            messages.add_message(request, messages.ERROR, 'An error ocurred while creating the question')
        return self.get(request, *args, **kwargs)
    

#class SimpleTextQuestionResp(QuestionViewResp):
class SimpleQuestionViewResp(QuestionViewResp):
    template_name = 'responsable/simple_text_question.html'
    name = 'simple_text_question'
    form_class = SimpleTextAnswerForm

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
            answer.report = ReportByProject.objects.first()
            self.answer = answer
            self.save(answer)
            messages.add_message(request, messages.SUCCESS, 'Question answered successfully')
        else:
            print(form.errors)
            messages.add_message(request, messages.ERROR, 'An error ocurred while answering the question')

        return self.get(request, *args, **kwargs)


#class SimpleTextQuestionPDF(QuestionViewPDF):
class SimpleTextQuestionPDF(QuestionViewPDF):
    name = 'simple_text_question'
    template_name = 'pdf/simple_text_question.html'

    def get(self, request, *args, **kwargs):
        self.request = request
        self.question = Question.objects.get(pk=kwargs['question_pk'])
        self.answer = Answer.objects.filter(question=self.question).first()

        parameters = {
            'name': self.name,
            'question': self.question,
            'question_number': self.question.order,
            'answer': self.answer,
            'form_number': str(random.randint(self.start_number, self.end_number)),
            'datetime': timezone.now(),
        }

        template = get_template(self.template_name)

        html = template.render(Context(parameters)).encode('UTF-8')

        page = HTML(string=html, encoding='utf-8').write_pdf()

        response = HttpResponse(page, content_type='application/pdf')

        response[
            'Content-Disposition'] = 'attachment; filename="question_report.pdf"'

        return response
