import json

from django.utils.translation import ugettext as _
from report_builder.Question.QuestionView import QuestionViewAdmin, QuestionViewReviewer, QuestionViewCSV, \
    QuestionViewJSON, QuestionViewSPSS
from report_builder.Question.QuestionView import QuestionViewResp
from report_builder.Question.QuestionView import QuestionViewPDF
from report_builder.Question.forms import BooleanAnswerForm
from report_builder.shortcuts import get_children


class BooleanQuestionViewAdmin(QuestionViewAdmin):
    template_name = 'admin/question_types/boolean_question.html'
    name = 'boolean_question'
    minimal_representation = {
        'human_readable_name': _('Yes/No question'),
        'help': _('Allows you to make yes/no questions'),
        'color': '#5b4e77'
    }

    def pre_save(self, object, request, form):
        children = get_children(form)
        if children is not None:
            object.answer_options = json.dumps({"children": children})
        return object

    def additional_template_parameters(self, **kwargs):
        parameters = self.get_question_answer_options()
        if not parameters:
            parameters = {}

        parameters['children'] = self.process_children(self.request,
                                                       parameters, kwargs)
        return parameters


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
