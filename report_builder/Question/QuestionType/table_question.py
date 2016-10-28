'''
Created on 20/10/2016

@author: adolfo
'''
import json

from django.utils.translation import ugettext as _

from report_builder.Question import QuestionView
from report_builder.Question.forms import TableQuestionForm

class TableQuestionViewAdmin(QuestionView.QuestionViewAdmin):
    form_class = TableQuestionForm
    template_name = 'admin/table_question.html'
    name = 'table_question'
    minimal_representation = {
        'human_readable_name': _('Table question'),
        'help': _('Allows you to make table questions'),
        'color': '#330065'
    }
    
    def pre_save(self, object, request, form):
        print(request.data)
        form_data = dict(form.data)
        answer_options = {
            'catalog': form_data.get('catalog'),
        }
        object.answer_options = json.dumps(answer_options)
        return object