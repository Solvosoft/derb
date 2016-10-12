'''
Created on 14/9/2016

@author: natalia
'''
import json
from report_builder.Question.QuestionView import QuestionViewAdmin, QuestionViewResp, QuestionViewPDF
from django.shortcuts import render, get_object_or_404
from report_builder.Question.forms import IntegerQuestionForm, AnswerForm
from report_builder.models import Report, Question, Answer, ReportByProject
from report_builder.shortcuts import get_children
import random
from django.contrib import messages
from _datetime import timezone
from django.template.loader import get_template

from django.http import HttpResponse
from django.template import Context
from weasyprint import HTML


class IntegerQuestionAdmin(QuestionViewAdmin):
    form_class = IntegerQuestionForm
    template_name = 'admin/integer_question.html'
    name = 'integer_question'
    minimal_representation = {
        'human_readable_name': 'Numerical question',
        'help': 'Allows you to make numerical questions',
        'color': '#330065'
    }

    def pre_save(self, object, request, form):
        form_data = dict(form.data)

        answer_options = {
            "maximum": int(form_data.get('maximum')[0]),
            "minimum": int(form_data.get('minimum')[0]),
            "steps": int(form_data.get('steps')[0]),
        }
        object.answer_options = json.dumps(answer_options)
        return object


class IntegerQuestionResp(QuestionViewResp):
    template_name = 'responsable/integer_question.html'
    name = 'integer_question'
    form_class = AnswerForm

    def get(self, request, *args, **kwargs):
        """
            TODO: docstring
        """
        self.request = request
        self.form_number = random.randint(self.start_number, self.end_number)
        self.question = get_object_or_404(Question, pk=kwargs['question_pk'])
        form = self.get_form(instance=self.answer)
        answer_options_json = self.question.answer_options
        answer_options = json.loads(answer_options_json)
        minimum = answer_options['minimum']
        maximum = answer_options['maximum']
        steps = answer_options['steps']
        answer = self.request.GET.get("integer_answer")
        parameters = {
            'integer_answer': answer,
            'minimum': minimum,
            'maximum': maximum,
            'steps': steps,
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
            integer_answer = self.request.POST.get("integer_answer")
            answer.text = str(integer_answer)
            answer.annotation = str(integer_answer)
            answer.display_text = str(integer_answer)
            self.answer = answer
            self.save(answer)
            messages.add_message(request, messages.SUCCESS, 'Question answered successfully')
        else:
            messages.add_message(request, messages.ERROR, 'An error ocurred while answering the question')

        return self.get(request, *args, **kwargs)


class IntegerQuestionViewPDF(QuestionViewPDF):
    name = 'integer_question'
    template_name = 'pdf/integer_question.html'

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
            # 'datetime': timezone.now(),
        }

        template = get_template(self.template_name)

        html = template.render(Context(parameters)).encode('UTF-8')

        page = HTML(string=html, encoding='utf-8').write_pdf()

        response = HttpResponse(page, content_type='application/pdf')

        response[
            'Content-Disposition'] = 'attachment; filename="question_report.pdf"'

        return response
