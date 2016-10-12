import random

from django.http import HttpResponse
from django.template.loader import get_template
from django.utils import timezone

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

class BooleanQuestionViewResp(QuestionViewResp):
    template_name = 'responsable/boolean_question.html'
    name = 'boolean_question'
    form_class = BooleanAnswerForm


class BooleanQuestionViewPDF(QuestionViewPDF):
    name = 'boolean_question'
    template_name = 'pdf/boolean_question.html'
