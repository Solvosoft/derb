'''
Created on 15/9/2016

@author: nashyra
'''
import json
import random

from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.template import Context
from django.template.loader import get_template
from django.utils import timezone
from weasyprint import HTML

from report_builder.Question.QuestionView import QuestionViewAdmin, QuestionViewResp, QuestionViewPDF
from report_builder.Question.forms import SimpleTextQuestionForm, SimpleTextAnswerForm
from report_builder.models import Question, Answer



class SimpleTextQuestionAdmin(QuestionViewAdmin):
    form_class = SimpleTextQuestionForm
    template_name = 'admin/simple_text_question.html'
    name = 'simple_text_question'
    minimal_representation = {
        'human_readable_name': 'Simple text question',
        'help': 'Allows you to make simple text questions',
        'color': '#330065'
    }

#class SimpleTextQuestionResp(QuestionViewResp):
class SimpleQuestionViewResp(QuestionViewResp):
    template_name = 'responsable/simple_text_question.html'
    name = 'simple_text_question'
    form_class = SimpleTextAnswerForm


#class SimpleTextQuestionPDF(QuestionViewPDF):
class SimpleTextQuestionPDF(QuestionViewPDF):
    name = 'simple_text_question'
    template_name = 'pdf/simple_text_question.html'
