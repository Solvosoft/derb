from report_builder.models import QuestionInfoRelation


def get_question_with_permission(questions, parent):
    try:
        question = questions[parent]
    except:
        relation = QuestionInfoRelation.objects.filter(question__pk=parent)
        question = get_question_with_permission(questions, relation[0].parent_question.pk)
    return question


def get_question_permission(question):
    """
        TODO: docstring
    """
    questions = question.report.questions
    return_value = question.required
    parent = question.pk
    if return_value == 2:
        while (return_value == 2):
            question = get_question_with_permission(questions, parent)
            parent = question['parent']
            if parent == -1:
                return_value = 0
            else:
                return_value = questions[parent]['required']
    return return_value
