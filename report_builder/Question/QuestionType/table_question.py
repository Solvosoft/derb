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
        form_data = dict(form.data)
        headers = []
        displays = []
        for key in form_data.keys():
            if key.startswith('header_'):
                headers += [key]
            if key.startswith('display_field_'):
                displays += [key]       
        headers_1 = sorted(headers)
        displays_1 = sorted(displays)
        headers = []
        displays = []
        for head in headers_1:
            headers += form_data[head]
        for display in displays_1:
            displays += form_data[display]
        print(headers)
        print(displays)
        answer_options = {
            'catalog': form_data.get('catalog'),
            'headers': headers,
            'displays': displays
        }
        object.answer_options = json.dumps(answer_options)
        return object


    def get_form(self, post=None, instance=None, extra=None):
        if post is not None:
            count = 0
            post_data = dict(post)
            for key in list(post_data.keys()):
                if key.startswith('header_'):
                    count = count + 1
        else:
            count = 1

        if post is not None:
            form = self.form_class(post, instance=instance, extra=count)
        else:
            form = self.form_class(instance=instance, extra=count)
        return form
