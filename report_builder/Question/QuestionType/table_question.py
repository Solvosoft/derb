'''
Created on 20/10/2016

@author: adolfo
'''
import json

from django.utils.translation import ugettext as _

from report_builder.Question import QuestionView
from report_builder.Question.forms import TableQuestionForm, TableQuestionAnswerForm
from report_builder.registry import models

def get_catalog_values(queryset, display_fields):
    '''
    This function returns a generator whit the values found in the database,
    according whit the fields ("display_fields") of each corresponding model ("queryset").
    '''
    for object in queryset:
        text = ""
        value = object.pk
        if display_fields is None:
            yield (value, str(object))
        else:
            text += getattr(object, display_fields)
            yield (value, text)


def get_catalog_choices(catalog, display):
    '''
    This function receives two values.
    The "catalog" is used to define the value of the list "models" that will be used.
    Both data, will be sent to be used in the method "get_catalog_values".  
    '''
    catalog_id = int(catalog)
    display_fields = display
    queryset = models[catalog_id][0]

    return (value_text for value_text in get_catalog_values(queryset, display_fields))


class TableQuestionViewAdmin(QuestionView.QuestionViewAdmin):
    '''
    TableQuestionViewAdmin class represents the implementation of the template administrator view 
    for a table question.
    By itself, this view provides the functionality for create, edit and delete the question.
    
    This class extends from another class, using an implemention like this:
    
    .. code:: python

        from report_builder.Question import QuestionView
        class TableQuestionViewAdmin(QuestionView.QuestionViewAdmin):
            template_name = 'admin/question_types/table_question.html'
            name = 'table_question'
    
    This class overrides functions of the Question class (report_builder/Question/QuestionView):
    
    .. code:: python
        
        def pre_save(self, object, request, form)
        def get_form(self, post=None, instance=None, extra=None)
    '''
    
    form_class = TableQuestionForm
    template_name = 'admin/question_types/table_question.html'
    name = 'table_question'
    minimal_representation = {
        'human_readable_name': _('Table question'),
        'help': _('Allows you to make table questions'),
        'color': '#FFA500'
    }
    
    def pre_save(self, object, request, form):
        '''
        It allows sort and save the headers and display_fields obtained from the form, through lists.
        '''
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

class TableQuestionViewResp(QuestionView.QuestionViewResp):
    '''
    TableQuestionViewResp class represents the implementation of the template responsable view 
    for a table question.
    By itself, this view shows the table question created by the template administrator and 
    it allows the user to answer the question.
    
    This class extends from another class, using an implemention like this:
    
    .. code:: python

        from report_builder.Question import QuestionView
        class TableQuestionViewResp(QuestionView.QuestionViewResp):
            template_name = 'responsable/table_question.html'
            name = 'table_question'
            
    This class override one function of the Question class (report_builder/Question/QuestionView):
    
    .. code:: python
        
        def get_form(self, post=None, instance=None, extra=None)
    '''
    
    template_name = 'responsable/table_question.html'
    name = 'table_question'
    form_class = TableQuestionAnswerForm
    
    def get_form(self, post=None, instance=None, extra=None):
        '''
        Use the data in "answer_options" to extract specific information in the database, and passes this
        information to the form of the class.
        '''
        answer_options = json.loads(self.question.answer_options)
        headers = answer_options['headers']
        displays = answer_options['displays']
        catalog = answer_options['catalog'][0]
        catalog_choices = []
        elements = []
        for dis in displays:
            for x in get_catalog_choices(catalog, dis):
                elements.append(x)
            catalog_choices.append(elements)
            elements = []

        extra = {
            'headers': headers,
            'displays': displays,
            'catalog_choices': catalog_choices
        }
            
        if post is not None:
            form = self.form_class(post, instance=instance, extra=extra)
        else:
            form = self.form_class(instance=instance, extra=extra)
        return form       
    
class TableQuestionViewPDF(QuestionView.QuestionViewPDF):
    '''
    TableQuestionViewPDF class represents the implementation of exporting a table question
    to a PDF document.
    
    This class extends from another class, using an implemention like this:
    
    .. code:: python

        from report_builder.Question import QuestionView
        class TableQuestionViewPDF(QuestionView.QuestionViewPDF):
            template_name = 'pdf/table_question.html'
            name = 'table_question'
    '''
    name = 'table_question'
    template_name = 'pdf/table_question.html'
    

class TableQuestionViewCSV(QuestionView.QuestionViewCSV):
    '''
    TableQuestionViewCSV class represents the implementation of exporting a question object to a CSV formatted string.
    
    This class extends from another class, using an implemention like this:
    
    .. code:: python

        from report_builder.Question import QuestionView
        class TableQuestionViewCSV(QuestionView.QuestionViewCSV):
            name = 'table_question'
    '''
    name = 'table_question'


class TableQuestionViewJSON(QuestionView.QuestionViewJSON):
    '''
    TableQuestionViewJSON class represents the implementation of exporting a question object to a JSON formatted string.
    
    This class extends from another class, using an implemention like this:
    
    .. code:: python

        from report_builder.Question import QuestionView
        class TableQuestionViewJSON(QuestionView.QuestionViewJSON):
            name = 'table_question'
    '''
    name = 'table_question'

