'''
Created on 15/9/2016
@author: nashyra
'''
import json
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django_ajax.decorators import ajax
from django.template.loader import render_to_string

from report_builder.Question.QuestionView import QuestionViewAdmin, QuestionViewResp, QuestionViewPDF, QuestionViewReviewer, QuestionViewCSV,QuestionViewJSON
from report_builder.Question.forms import SimpleTextQuestionForm, SimpleTextAnswerForm
from report_builder.models import Question
from report_builder.models import Answer, Observation, Reviewer


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
        object.answer_options = json.dumps({'on_modal': form.cleaned_data['on_modal']})
        object.required = Question.OPTIONAL
        return object

    def additional_template_parameters(self, **kwargs):
        return {}


# class SimpleTextQuestionResp(QuestionViewResp):
class SimpleQuestionViewResp(QuestionViewResp):
    name = 'simple_text_question'
    template_name = 'responsable/simple_text_question.html'
    form_class = SimpleTextAnswerForm


# class SimpleTextQuestionPDF(QuestionViewPDF):
class SimpleTextQuestionViewPDF(QuestionViewPDF):
    name = 'simple_text_question'
    template_name = 'pdf/simple_text_question.html'
    

class SimpleTextQuestionViewReviewer(QuestionViewReviewer):
    name = 'simple_text_question'
    template_name = 'revisor/simple_text_question.html'
    

@ajax
@csrf_exempt
def submit_new_observation(request):
    if request.is_ajax():
        if request.method == 'POST':
            report_pk = request.POST.get('report_pk', False)
            question_pk = request.POST.get('question_pk', False)
            answer_pk = request.POST.get('answer_pk', False)
            observation = request.POST.get('observation', False)

            print(report_pk, question_pk, answer_pk)

            if report_pk and question_pk and answer_pk:
                answer = Answer.objects.get(pk=answer_pk)
                reviewer = Reviewer.objects.get(report__pk=report_pk, user=request.user)

                observation = Observation.objects.create(
                    reviewer=reviewer,
                    text=observation,
                    answer=answer
                )
                rendered = render_to_string('revisor/observations.html', {'observation': observation})

                return rendered
            else:
                return False

    return HttpResponse(0)

class SimpleQuestionViewCSV(QuestionViewCSV):
    name = 'simple_text_question'
    

class SimpleQuestionViewJSON(QuestionViewJSON):
    name = 'simple_text_question'
    
