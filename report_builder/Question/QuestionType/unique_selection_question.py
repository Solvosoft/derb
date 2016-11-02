'''
Created on 14/9/2016
@author: adolfo
'''
import json
from django_ajax.decorators import ajax
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.template.loader import render_to_string

from report_builder.Question import QuestionView
from report_builder.Question.forms import UniqueSelectionQuestionForm
from report_builder.Question.forms import UniqueSelectionAnswerForm
from report_builder.registry import models
from report_builder.models import Answer, Observation, Reviewer


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


class UniqueSelectionQuestionViewAdmin(QuestionView.QuestionViewAdmin):
    form_class = UniqueSelectionQuestionForm
    template_name = 'admin/unique_selection_question.html'
    name = 'unique_selection_question'
    minimal_representation = {
        'human_readable_name': 'Unique Selection Question',
        'help': 'Allows you to make unique selection questions',
        'color': '#330065'
    }

    def pre_save(self, object, request, form):
        form_data = dict(form.data)
        answer_options = {
            'catalog': form_data.get('catalog'),
            'display_fields': form_data.get('display_fields')
        }
        object.answer_options = json.dumps(answer_options)
        return object


class UniqueSelectionQuestionViewResp(QuestionView.QuestionViewResp):
    template_name = 'responsable/unique_selection_question.html'
    name = 'unique_selection_question'
    form_class = UniqueSelectionAnswerForm

    def get_form(self, post=None, instance=None, extra=None):
        catalog_choices = get_catalog_choices(self.question.answer_options)
        if post is not None:
            form = self.form_class(post, instance=instance, extra=catalog_choices)
        else:
            form = self.form_class(instance=instance, extra=catalog_choices)
        return form


class UniqueSelectionQuestionViewPDF(QuestionView.QuestionViewPDF):
    name = 'unique_selection_question'
    template_name = 'pdf/unique_selection_question.html'


@ajax
def get_catalog_display_fields(request):
    if request.method == 'GET':
        if request.is_ajax():
            catalog_id = request.GET.get('catalog_id', False)
            if catalog_id.isdigit():
                catalog_id = int(catalog_id)
                if catalog_id >= 0 and catalog_id < len(models):
                    catalog = models[catalog_id]
                    return catalog[3]
    return ()


class UniqueSelectionQuestionViewReviewer(QuestionView.QuestionViewReviewer):
    name = 'unique_selection_question'
    template_name = 'revisor/unique_selection_question.html'
    
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
                rendered = render_to_string('revisor/observations.html', {'observations': observation})

                return rendered
            else:
                return False

    return HttpResponse(0)


class UniqueQuestionViewCSV(QuestionView.QuestionViewCSV):
    name = 'unique_selection_question'
    

class UniqueQuestionViewJSON(QuestionView.QuestionViewJSON):
    name = 'unique_selection_question'