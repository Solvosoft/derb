'''
Created on 20/10/2016

@author: adolfo
'''
import json
from django_ajax.decorators import ajax
from django.utils.translation import ugettext as _

from report_builder.Question import QuestionView
from report_builder.Question.forms import TableQuestionForm
from report_builder.registry import models

class TableQuestionViewAdmin(QuestionView.QuestionViewAdmin):
    form_class = TableQuestionForm
    template_name = 'admin/table_question.html'
    name = 'table_question'
    minimal_representation = {
        'human_readable_name': _('Table Question'),
        'help': _('Allows you to make table questions'),
        'color': '#330065'
    }