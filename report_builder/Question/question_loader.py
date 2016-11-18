from django.http import Http404
from report_builder.models import Question, Answer
from report_builder.shortcuts import transform_request_to_get

registered_views = {}
has_answer = ['responsable', 'pdf', 'reviewer']

'''
This module is used to manage question types views. It  allows to render from a reversed URL or internally if the
questions extend from others.

The module has ``registered_views`` which are loaded when Django starts, this a dict that is build with the
function :func:`.register_view` and looks like this:

.. code:: python

    registered_views = {
        'admin': [
            Class report_builder.Question.QuestionType.boolean_question.BooleanQuestionViewAdmin,
            Class report_builder.Question.QuestionType.float_question.FloatQuestionViewAdmin,
            Class report_builder.Question.QuestionType.integer_question.IntegerQuestionViewAdmin,
            ...
        ],
        'responsable': [
            Class report_builder.Question.QuestionType.boolean_question.BooleanQuestionViewResp,
            Class report_builder.Question.QuestionType.float_question.FloatQuestionViewResp,
            Class report_builder.Question.QuestionType.integer_question.IntegerQuestionViewResp,
        ],
        'revisor': [
            Class report_builder.Question.QuestionType.boolean_question.BooleanQuestionViewRevisor,
            Class report_builder.Question.QuestionType.float_question.FloatQuestionViewRevisor,
            Class report_builder.Question.QuestionType.integer_question.IntegerQuestionViewRevisor,
        ]
    }

'''


def get_view_type(view_type):
    '''
    Gets a list of views that match the type given

    :raise KeyError if the type doesn't match any type in the registered views list
    :param str view_type:  name of the view type to lookup
    :rtype List
    :return: list of views for the type given
    '''

    if view_type in registered_views:
        return registered_views[view_type]
    else:
        raise KeyError('view_type', 'View type not registered')


def register_view(view, view_type='admin', with_answer=False):
    '''
    Adds question type views to the registered views to be managed for the application.

    .. code:: python

        from report_builder.Question.question_loader import register_view
        from report_builder.Question.QuestionView import QuestionViewAdmin, QuestionViewResp

        register_view(QuestionViewAdmin, view_type='admin')
        register_view(QuestionViewResp, view_type='responsable', with_answer=True)

    .. note::
        The question type views classes need to be defined with an attribute name

    .. warning::
        If there two views with the same name attribute, the last one is the only one loaded to registered views

    :param Class view: class that handles the view
    :param str view_type: name of the view type to store in registered views
    :param with_answer: specifies if this view requires the pk of the answer object related to the question
    :return:
    '''
    if not view_type in registered_views:
        registered_views[view_type] = {}

    views = get_view_type(view_type)
    views[view.name] = view
    if with_answer:
        if not view_type in has_answer:
            has_answer.append(view_type)


def get_view(*args, **kwargs):
    '''
    Gets the view that matches the ``type`` and ``view_type`` in the registered views
    :param kwargs: type (category of the view) and view_type (unique id for the view)
    :return:
    :raise Http404 if the parameters given matches the ``type`` and ``view_type`` in the registered views
    '''
    if not 'type' in kwargs:
        raise Http404
    views = get_view_type(kwargs['type'])

    if not 'view_type' in kwargs:
        raise Http404
    view_type = kwargs['view_type']

    if not view_type in views:
        raise Http404

    return views[view_type]


def process_question(request, *args, **kwargs):
    '''
    Renders a view and returns its content

    :param request: HTTP request passed to the view
    :param args: arguments passed to the view
    :param kwargs: keyword arguments passed to the view, type (category of the view) and view_type (unique id for the view)
    :return: content returned of the view
    '''
    view = get_view(*args, **kwargs).as_view()
    return_value = view(request, *args, **kwargs)
    return return_value


def process_questions(request, report, question_list, view_type='admin', reportbyproj=None):
    '''
    Renders the question list (``question_list``) of a ``report`` according to a given ``type``
    If ``reportbyproj`` is provided, it looks for the question answer in such report

    :param request: HTTP request passed to the question views
    :param report: report that contains the question
    :param question_list: question pk list meant to be rendered
    :param view_type: category of the view
    :param reportbyproj: report by project to get the questions' answers
    :return: a list with the HTML content returned for every question view for every pk in the list provided
    '''
    request = transform_request_to_get(request)
    questions_html = []
    args = {}
    report_pk = report
    for question_pk in question_list:
        question = Question.objects.get(pk=question_pk)
        if reportbyproj is not None:
            report_pk = reportbyproj.pk

        kwargs = {
            'report_pk': report_pk,
            'question_pk': question_pk,
            'view_type': question.class_to_load,
            'type': view_type
        }
        if view_type in has_answer:
            answers = Answer.objects.filter(user=request.user, question=question, report=reportbyproj.pk)
            if len(answers) > 0:
                kwargs['answer_pk'] = answers[0].pk
            else:
                kwargs['anwser_pk'] = None
        processed = process_question(request, *args, **kwargs)
        questions_html.append(processed.content)

    return questions_html
