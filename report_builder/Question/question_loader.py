from django.http import Http404
from report_builder.models import Question, Answer
from report_builder.shortcuts import transform_request_to_get

registered_views = {
    'admin': {}
}
has_answer = ['responsable', 'pdf', 'reviewer']


def get_view_type(view_type):
    """
        TODO docstring
    """
    if view_type in registered_views:
        return registered_views[view_type]
    else:
        raise KeyError('view_type', 'View type not registered')


def register_view(view, view_type='admin', with_answer=False):
    """
        TODO docstring
    """
    if not view_type in registered_views:
        registered_views[view_type] = {}

    views = get_view_type(view_type)
    views[view.name] = view
    if with_answer:
        if not view_type in has_answer:
            has_answer.append(view_type)


def get_view(*args, **kwargs):
    """
        TODO docstring
    """
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
    """
        TODO docstring
    """
    view = get_view(*args, **kwargs).as_view()
    return_value = view(request, *args, **kwargs)
    return return_value


def process_questions(request, report, question_list, view_type='admin', reportbyproj=None):
    """
        TODO docstring
    """
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
