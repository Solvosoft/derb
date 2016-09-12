import ast
import copy
from collections import OrderedDict

import datetime
import re
from django.shortcuts import get_object_or_404
from report_builder.models import ReportByProject, Answer
from report_builder.models import Report
from report_builder.models import Question
from report_builder.models import Reviewer

question_list = {}


def get_report_question(pk, question=None):
    """
        TODO: docstring
    """
    report = get_object_or_404(Report, pk=pk)
    if question:
        question = get_object_or_404(Question, pk=question)
    return report, question


def get_reportbyproj_question_answer(report_pk, question_pk, answer_pk=None):
    """
        TODO: docstring
    """
    reportbyproj = get_object_or_404(ReportByProject, pk=report_pk)
    question = get_object_or_404(Question, pk=question_pk)
    answer = None
    if answer_pk is not None:
        answer = get_object_or_404(Answer, pk=answer_pk, report=reportbyproj)
    else:
        answer_queryset = Answer.objects.filter(report=reportbyproj, question=question)
        try:
            answer = answer_queryset[0]
        except:
            answer = None
    return reportbyproj, question, answer


def transform_request_to_get(request):
    """
    Builds a requests from another, forcing the new one to use the GET HTTP method
    """
    request = copy.copy(request)
    request.POST = request.GET
    request.META['REQUEST_METHOD'] = 'GET'
    request.method = 'GET'
    return request


def get_children(form):
    """
        TODO: docstring
    """
    children = None
    if hasattr(form, 'cleaned_data') and 'children' in form.cleaned_data and form.cleaned_data['children']:
        children = OrderedDict(ast.literal_eval(form.cleaned_data['children']))
    return children


def get_reportbyproject_questions(report_pk, question_pk=None):
    """
        TODO: docstring
    """
    reportbyproj = get_object_or_404(ReportByProject, pk=report_pk)
    question = None
    if question_pk is not None:
        question = get_object_or_404(Question, pk=question_pk)
    return reportbyproj, question


def get_active_reviewer(reportbyproj, user):
    """
    Check if the logged user is a reviewer of the project, in which case returns it. Otherwise returns None
    """
    reviewers = Reviewer.actives.filter(report=reportbyproj, user=user)
    rev = None
    if len(reviewers) > 0:
        rev = reviewers[0]
    return rev


def get_reviewers_by_user(user):
    '''
        TODO: docstring
    '''
    return Reviewer.actives.filter(user=user)


def get_reviewers_by_report(reportbyproj):
    '''
        TODO: docstring
    '''
    return Reviewer.actives.filter(report=reportbyproj).order_by('order')


def copy_report(report):
    '''
        TODO: docstring
    '''
    today = datetime.date.today()
    tomorrow = today + datetime.timedelta(days=1)
    new = Report.objects.create(type=report.type, name=report.name + '_copy', opening_date=tomorrow)
    question_list = []
    global question_list

    questions = {}
    for quest in report.questions:
        question_list.append(quest)

    questions_to_copy = Question.objects.filter(pk__in=questions)

    for quest in questions_to_copy:
        if quest.pk in questions:
            continue
        q = copy_questions(quest.answer_options, new)
        new = Question.objects.create(report=new,
                                      class_to_load=quest.class_to_load,
                                      text=quest.text,
                                      help=quest.help,
                                      required=quest.required,
                                      order=quest.order,
                                      answer_options=q
                                      )
        questions[quest.pk] = new.pk

    new.questions = {}
    for x in report.questions:
        new_pk = questions[x]
        new.questions[new_pk] = report.questions[x]
        if report.questions[x]['parent'] != -1:
            new.questions[new_pk]['parent'] = questions[report.questions[x]['parent']]

    new_template = []
    for template in report.template:
        pass


def copy_questions(text, report):
    '''
        TODO: docstring
    '''
    found = []
    new = text
    p = re.compile('[\[|\(]{1}((?P<preg>\d+)[,\s]*)+[\]|\)]{1}')
    m = p.finditer(text)
    for x in m:
        (px, py) = x.span()
        found.append((text[px:py], get_new_questions(text[px:py], report)))

    for x in found:
        new = new.replace(x[0], x[1])

    return new


def get_new_questions(text_list, report):
    '''
        TODO: docstring
    '''
    copied_questions = ''
    new = '[%s]'
    if '(' in text_list:
        new = '(%s)'

    ex = re.compile('\d+')
    em = ex.finditer(text_list)
    for x in em:
        (px, py) = x.span()
        pk = int(text_list[px:py])
        copied_questions += str(get_question_copy(pk, report)) + ', '

    if ',' in copied_questions[:-2]:
        copied_questions = copied_questions[:-2]

    return new % (copied_questions)


def get_question_copy(pk, report):
    '''
        TODO: docstring
    '''
    global question_list

    if pk in question_list:
        return question_list[pk]

    question = Question.objects.get(pk=pk)
    new = Question.objects.create(report=report,
                                  class_to_load=question.class_to_load,
                                  text=question.text,
                                  help=question.help,
                                  required=question.required,
                                  order=question.order,
                                  answer_options=copy_questions(question.answer_options, report))
    question_list[pk] = new.pk
    return new.pk
