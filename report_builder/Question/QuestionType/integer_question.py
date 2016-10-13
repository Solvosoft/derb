'''
Created on 14/9/2016
@author: natalia
'''
import json
from report_builder.Question.QuestionView import QuestionViewAdmin, QuestionViewResp, QuestionViewPDF
from report_builder.Question.forms import IntegerQuestionForm, AnswerForm, IntegerAnswerForm


class IntegerQuestionAdmin(QuestionViewAdmin):
    form_class = IntegerQuestionForm
    template_name = 'admin/integer_question.html'
    name = 'integer_question'
    minimal_representation = {
        'human_readable_name': 'Numerical question',
        'help': 'Allows you to make numerical questions',
        'color': '#330065'
    }
    evaluator = int

    def pre_save(self, object, request, form):
        form_data = dict(form.data)

        answer_options = {
            "maximum": self.evaluator(form_data.get('maximum')[0]),
            "minimum": self.evaluator(form_data.get('minimum')[0]),
            "steps": self.evaluator(form_data.get('steps')[0]),
        }
        object.answer_options = json.dumps(answer_options)
        return object


class IntegerQuestionResp(QuestionViewResp):
    template_name = 'responsable/integer_question.html'
    name = 'integer_question'
    form_class = IntegerAnswerForm

    def get_form(self, post=None, instance=None, extra=None):
        answer_options_json = self.question.answer_options
        answer_options = json.loads(answer_options_json)
        if post is not None:
            form = self.form_class(post, instance=instance, extra=answer_options)
        else:
            form = self.form_class(instance=instance, extra=answer_options)
        return form


class IntegerQuestionViewPDF(QuestionViewPDF):
    name = 'integer_question'
    template_name = 'pdf/integer_question.html'
