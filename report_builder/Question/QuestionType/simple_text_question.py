'''
Created on 15/9/2016
@author: nashyra
'''
from report_builder.Question.QuestionView import QuestionViewAdmin, QuestionViewResp, QuestionViewPDF
from report_builder.Question.forms import SimpleTextQuestionForm, SimpleTextAnswerForm
from report_builder.models import Question


class SimpleTextQuestionViewAdmin(QuestionViewAdmin):
    form_class = SimpleTextQuestionForm
    template_name = 'admin/question_types/simple_text_question.html'
    name = 'simple_text_question'
    minimal_representation = {
        'human_readable_name': 'Simple text question',
        'help': 'Allows you to make simple text questions',
        'color': '#88a05b'
    }

    def get_form(self, post=None, instance=None, extra=None):
        on_modal = self.get_question_answer_options()
        if on_modal is None:
            on_modal = False

        extra = {
            'form_number': str(self.form_number),
            'on_modal': on_modal
        }

        return super(SimpleTextQuestionViewAdmin, self).get_form(post=post, instance=instance, extra=extra)

    def pre_save(self, object, request, form):
        object.text = form.cleaned_data['text']
        object.answer_options = repr(form.cleaned_data['on_modal'])
        object.required = Question.OPTIONAL
        return object

    def additional_template_parameters(self, **kwargs):
        return {}


# class SimpleTextQuestionResp(QuestionViewResp):
class SimpleQuestionViewResp(QuestionViewResp):
    template_name = 'responsable/simple_text_question.html'
    name = 'simple_text_question'
    form_class = SimpleTextAnswerForm


# class SimpleTextQuestionPDF(QuestionViewPDF):
class SimpleTextQuestionViewPDF(QuestionViewPDF):
    name = 'simple_text_question'
    template_name = 'pdf/simple_text_question.html'