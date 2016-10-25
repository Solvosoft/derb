'''
Created on 18/10/2016

@author: natalia
'''
from report_builder.Question import QuestionView
from report_builder.Question.forms import MultipleSelectionQuestionForm,\
    MultipleSelectionAnswerForm
import json
from report_builder.Question.QuestionType.unique_selection_question import get_catalog_choices

class MultipleSelectionQuestionViewAdmin(QuestionView.QuestionViewAdmin):
    form_class = MultipleSelectionQuestionForm
    template_name = 'admin/multiple_selection_question.html'
    name = 'multiple_selection_question'
    minimal_representation = {
        'human_readable_name': 'Multiple Selection Question',
        'help': 'Allows you to make multiple selection questions',
        'color': '#330065'
    }
    
    def pre_save(self, object, request, form):
        form_data = dict(form.data)
        answer_options = {
            'catalog': form_data.get('catalog'),
            'display_fields': form_data.get('display_fields'),
            "widget": form_data.get('widget')[0],
        }
        object.answer_options = json.dumps(answer_options)
        return object
    
class MultipleSelectionQuestionViewResp(QuestionView.QuestionViewResp):
    template_name = 'responsable/multiple_selection_question.html'
    name = 'multiple_selection_question'
    form_class = MultipleSelectionAnswerForm

    def get_form(self, post=None, instance=None, extra=None):
        catalog_choices = get_catalog_choices(self.question.answer_options)
        if post is not None:
            form = self.form_class(post, instance=instance, extra=catalog_choices)
        else:
            form = self.form_class(instance=instance, extra=catalog_choices)
        return form