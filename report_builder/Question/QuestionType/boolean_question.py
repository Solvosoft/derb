import random

from django.http import HttpResponse
from django.template import Context
from django.template.loader import get_template
from django.utils import timezone
from django.utils.translation import ugettext as _
from weasyprint import HTML

from report_builder.Question.QuestionView import QuestionViewAdmin, QuestionViewReviewer
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
        'color': '#5b4e77'
    }


class BooleanQuestionViewResp(QuestionViewResp):
    template_name = 'responsable/boolean_question.html'
    name = 'boolean_question'
    form_class = BooleanAnswerForm


class BooleanQuestionViewPDF(QuestionViewPDF):
    name = 'boolean_question'
    template_name = 'pdf/boolean_question.html'

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


class BooleanQuestionViewReviewer(QuestionViewReviewer):
    name = 'boolean_question'
    template_name = 'reviewer/boolean_question.html'