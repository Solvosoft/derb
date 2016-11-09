'''
Created on 14/9/2016
@author: adolfo
'''
import json
from django_ajax.decorators import ajax
from django.utils.translation import ugettext as _
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.template.loader import render_to_string
from report_builder.Question import QuestionView
from report_builder.Question.forms import UniqueSelectionQuestionForm
from report_builder.Question.forms import UniqueSelectionAnswerForm
from report_builder.registry import models
from report_builder.shortcuts import get_children
from report_builder.models import Answer, Observation, Reviewer


def get_catalog_values(queryset, display_fields):
    for object in queryset:
        text = ""
        value = object.pk
        if display_fields is None:
            yield (value, str(object))
        else:
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
    template_name = 'admin/question_types/unique_selection_question.html'
    name = 'unique_selection_question'
    minimal_representation = {
        'human_readable_name': _('Unique Selection Question'),
        'help': _('Allows you to make unique selection questions'),
        'color': '#fde95c'
    }
    widgets = (
        ('radiobox', 'Radio selection'),
        ('combobox', 'Dropdown selection'),
        ('select', 'Displayed list')
    )

    def additional_template_parameters(self, **kwargs):
        parameters = super(UniqueSelectionQuestionViewAdmin, self).additional_template_parameters(**kwargs)
        if parameters is None:
            parameters = {}
        report_type = self.report.type
        name = report_type.app_name + '.' + report_type.name
        parameters.update({
            'widgets': self.widgets
        })
        return parameters


    def pre_save(self, object, request, form):
        form_data = dict(form.data)
        # Widget
        widget = None
        if 'widget' in form_data:
            widget = form_data['']

        # Schema
        schema = ''
        if 'schema' in form_data:
            schema = form_data['schema']

        # Children questions
        children = get_children(form)

        answer_options = {
            'catalog': form_data.get('catalog'),
            'display_fields': form_data.get('display_fields'),
            'widget': widget,
            'children': children,
            'schema': schema
        }
        object.answer_options = json.dumps(answer_options)
        return object


    def get_form(self, post=None, instance=None, extra=None):
        answer_options = self.get_question_answer_options()
        if extra is None:
            extra = {}

        report_type = self.report.type
        name = report_type.app_name + '.' + report_type.name
        extra.update({
            'answer_options': answer_options,
            'widgets': self.widgets
        })

        return super(UniqueSelectionQuestionViewAdmin, self).get_form(post=post, instance=instance, extra=extra)


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
