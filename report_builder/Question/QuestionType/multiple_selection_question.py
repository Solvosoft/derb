'''
Created on 18/10/2016

@author: natalia
'''
from report_builder.Question import QuestionView
from report_builder.Question.forms import MultipleSelectionQuestionForm,\
    MultipleSelectionAnswerForm
import json
from report_builder.registry import models

def get_catalog_values(queryset, display_fields):
    for object in queryset:
        text = ""
        value = object.pk
        for i, field in enumerate(display_fields):
            text += getattr(object, field)
            if (i + 1) != len(display_fields):
                text += ' - '
        yield (value, text)


def get_catalog_choices(json_field):
    answer_options = json.loads(json_field)
    catalog = int(answer_options['catalog'][0])
    display_fields = answer_options['display_fields']
    queryset = models[catalog][0]

    return (value_text for value_text in get_catalog_values(queryset, display_fields))
class MultipleSelectionQuestionViewAdmin(QuestionView.QuestionViewAdmin):
    form_class = MultipleSelectionQuestionForm
    template_name = 'admin/multiple_selection_question.html'
    name = 'multiple_selection_question'
    minimal_representation = {
        'human_readable_name': 'Multiple Selection Question',
        'help': 'Allows you to make multiple selection questions',
        'color': '#330065'
    }
    
    evaluator = int
    def pre_save(self, object, request, form):
        form_data = dict(form.data)
        answer_options = {
            'catalog': form_data.get('catalog'),
            'display_fields': form_data.get('display_fields'),
            "widgett": self.evaluator(form_data.get('widgett')[0]),
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