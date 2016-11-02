'''
Created on 18/10/2016

@author: natalia
'''
from report_builder.Question import QuestionView
from report_builder.Question.forms import MultipleSelectionQuestionForm,\
    MultipleSelectionAnswerForm
from report_builder.Question.QuestionType.unique_selection_question import get_catalog_choices
import json
from report_builder.Question.QuestionView import QuestionViewPDF,\
    QuestionViewCSV, QuestionViewJSON, QuestionViewReviewer
from report_builder.models import Question, Answer
import random
from django.http import HttpResponse
from django.template import Context
from django.template.loader import get_template
from django.utils import timezone
from weasyprint import HTML

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
        catalog = get_catalog_choices(self.question.answer_options)
        answer_options_json = json.loads(self.question.answer_options)

        extra = {
            "catalog": catalog,
            "widget": answer_options_json['widget']
        }

        if post is not None:
            form = self.form_class(post, instance=instance, extra=extra)
        else:
            form = self.form_class(instance=instance, extra=extra)
        return form
    
class MultipleSelectionQuestionViewPDF(QuestionViewPDF):
    name = 'multiple_selection_question'
    template_name = 'pdf/multiple_selection_question.html'

    def get(self, request, *args, **kwargs):
        self.request = request
        self.question = Question.objects.get(pk=kwargs['question_pk'])
        self.answer = Answer.objects.filter(question=self.question).first()

        parameters = {
            'name': self.name,
            'question': self.question,
            'question_number': self.question.order,
            'answer': self.answer,
            'form_number': str(random.randint(self.start_number, self.end_number)),
            'datetime': timezone.now(),
        }

        template = get_template(self.template_name)

        html = template.render(Context(parameters)).encode('UTF-8')

        page = HTML(string=html, encoding='utf-8').write_pdf()

        response = HttpResponse(page, content_type='application/pdf')

        response[
            'Content-Disposition'] = 'attachment; filename="question_report.pdf"'

        return response

class MultipleSelectionQuestionViewCSV(QuestionViewCSV):
    name = 'multiple_selection_question'


class MultipleSelectionQuestionViewJSON(QuestionViewJSON):
    name = 'multiple_selection_question'

class MultipleSelectionQuestionViewReviewer(QuestionViewReviewer):
    name = 'multiple_selection_question'
    template_name = 'reviewer/multiple_selection_question.html'