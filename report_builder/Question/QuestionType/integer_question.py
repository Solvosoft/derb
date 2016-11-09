'''
Created on 14/9/2016
@author: natalia
'''
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django_ajax.decorators import ajax
from django.template.loader import render_to_string

import json
from report_builder.shortcuts import get_children
from report_builder.Question.QuestionView import QuestionViewAdmin, QuestionViewResp, QuestionViewPDF, QuestionViewReviewer, QuestionViewCSV, QuestionViewJSON
from report_builder.Question.forms import IntegerQuestionForm, IntegerAnswerForm
from report_builder.models import Answer, Observation, Reviewer


class IntegerQuestionViewAdmin(QuestionViewAdmin):
    form_class = IntegerQuestionForm
    template_name = 'admin/question_types/integer_question.html'
    name = 'integer_question'
    minimal_representation = {
        'human_readable_name': 'Numerical question',
        'help': 'Allows you to make numerical questions',
        'color': '#e86252'
    }
    evaluator = int

    def pre_save(self, object, request, form):
        children = get_children(form)

        form_data = dict(form.data)

        answer_options = {
            "maximum": self.evaluator(form_data.get('maximum')[0]),
            "minimum": self.evaluator(form_data.get('minimum')[0]),
            "steps": self.evaluator(form_data.get('steps')[0]),
            'children': children
        }
        object.answer_options = json.dumps(answer_options)
        return object

    def additional_template_parameters(self, **kwargs):
        parameters = self.get_question_answer_options()
        if not parameters:
            parameters = {}
        parameters['children'] = self.process_children(self.request, parameters, kwargs)
        return parameters

    def get_form(self, post=None, instance=None, extra=None):
        extra = self.get_question_answer_options()
        return super(IntegerQuestionViewAdmin, self).get_form(post=post, instance=instance, extra=extra)


class IntegerQuestionViewResp(QuestionViewResp):
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
    
    
class IntegerQuestionViewReviewer(QuestionViewReviewer):
    name = 'integer_question'
    template_name = 'revisor/integer_question.html'
    
@ajax
@csrf_exempt
def submit_new_observation(request):
    if request.is_ajax():
        if request.method == 'POST':
            report_pk = request.POST.get('report_pk', False)
            question_pk = request.POST.get('question_pk', False)
            answer_pk = request.POST.get('answer_pk', False)
            observation = request.POST.get('observation', False)

            if report_pk and question_pk and answer_pk:
                answer = Answer.objects.get(pk=answer_pk)
                reviewer = Reviewer.objects.get(report__pk=report_pk, user=request.user)

                observation = Observation.objects.create(
                    reviewer=reviewer,
                    text=observation,
                    answer=answer
                )
                rendered = render_to_string('revisor/observations.html', {'observations': observation})

                return rendered
            else:
                return False

    return HttpResponse(0)


class IntegerQuestionViewCSV(QuestionViewCSV):
    name = 'integer_question'
    

class IntegerQuestionViewJSON(QuestionViewJSON):
    name = 'integer_question'
