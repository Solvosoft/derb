import random

from django.http import HttpResponse
from django.template import Context
from django.template.loader import get_template
from django.utils import timezone
from django.utils.translation import ugettext as _
from weasyprint import HTML

from report_builder.Question.QuestionView import QuestionViewAdmin, QuestionViewReviewer, QuestionViewCSV, \
    QuestionViewJSON, QuestionViewSPSS
from report_builder.Question.QuestionView import QuestionViewResp
from report_builder.Question.QuestionView import QuestionViewPDF
from report_builder.Question.forms import BooleanAnswerForm
from report_builder.models import Question, Answer


class BooleanQuestionViewAdmin(QuestionViewAdmin):
    template_name = 'admin/boolean_question.html'
    name = 'boolean_question'
    minimal_representation = {
        'human_readable_name': _('Yes/No question'),
        'help': _('Allows you to make yes/no questions'),
        'color': '#330065'
    }


class BooleanQuestionViewResp(QuestionViewResp):
    template_name = 'responsable/boolean_question.html'
    name = 'boolean_question'
    form_class = BooleanAnswerForm


class BooleanQuestionViewPDF(QuestionViewPDF):
    name = 'boolean_question'
    template_name = 'pdf/boolean_question.html'


class BooleanQuestionViewReviewer(QuestionViewReviewer):
    name = 'boolean_question'
    template_name = 'reviewer/boolean_question.html'


class BooleanQuestionViewCSV(QuestionViewCSV):
    name = 'boolean_question'


class BooleanQuestionViewJSON(QuestionViewJSON):
    name = 'boolean_question'


class BooleanQuestionViewSPSS(QuestionViewSPSS):
    name = 'boolean_question'
