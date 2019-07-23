import threading
from report_builder.models import Question


def diff_list(before, after):
    '''
        TODO: docstring
    '''
    list = []
    for x in before:
        if x not in after:
            list.append(x)
    return list


def get_questions(question, save_questions=False):
    '''
        TODO: docstring
    '''
    pks = [int(question['pk'])]
    if save_questions:
        quest = Question.objects.filter(pk=int(question['pk'])).update(
            order=question['order']
        )

    if 'children' in question and question['children']:
        for key, value in question['children'].items():
            for q in value:
                pks += get_questions(q, save_questions)
    return pks


def get_report_questions(template, save_questions=False):
    '''
        TODO: docstring
    '''
    question_list = []
    for category in template:
        for subcategory in category['subcategories']:
            for question in subcategory['question']:
                question_list += get_questions(question, save_questions)
    print(question_list)
    return question_list


def get_question_children(question, category, subcategory, parent=1):
    '''
        TODO: docstring
    '''

    pk = int(question['pk'])
    quest = Question.objects.get(pk=pk)
    pks = [(pk, {
        'category': category,
        'subcategory': subcategory,
        'order': question['order'],
        'type': question['type'],
        'required': quest.required,
        'parent': parent,
        'state': -1
    }), ]

    if 'children' in question and question['children']:
        for key, value in question['children'].items():
            for question in value:
                pks += get_question_children(question, category, subcategory,
                                             parent=pk)

    return pks


def build_report_object(*args, **kwargs):
    '''
        TODO: docstring
    '''
    categories = kwargs['report'].template
    report_questions = {}

    for category in categories:
        for subcategory in category['subcategories']:
            if subcategory['question']:
                for question in subcategory['question']:
                    report_questions.update(
                        dict(get_question_children(question, category['name'],
                                                   subcategory['name'])))

    kwargs['report'].questions = report_questions
    kwargs['report'].save()


def delete_questions(*args, **kwargs):
    '''
        TODO: docstring
    '''
    questions_before = get_report_questions(kwargs['initial_template'])
    questions_after = get_report_questions(kwargs['final_template'], True)
    diff = diff_list(before=questions_before, after=questions_after)

    if diff:
        Question.objects.filter(pk__in=diff).delete()


def delete_questions_with_thread(initial_template, final_template):
    '''
        TODO: docstring
    '''
    report_dict = {
        'initial_template': initial_template,
        'final_template': final_template
    }
    thread = threading.Thread(target=delete_questions, kwargs=report_dict)
    thread.setDaemon(True)
    thread.start()


def build_report_object_with_thread(report):
    '''
        TODO: docstring
    '''
    report_dict = {
        'report': report
    }
    thread = threading.Thread(target=build_report_object, kwargs=report_dict)
    thread.setDaemon(True)
    thread.start()


def get_question_with_permission(questions, parent):
    '''
        try:
            question = questions[parent]
        except:
            relation = QuestionInfoRelation.objects.filter(question__pk=parent)
            question = get_question_with_permission(questions, relation[0].parent_question.pk)
        return question
        '''
    return


def get_question_permission(question):
    """
        TODO: docstring
    """
    '''
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
    '''
    return 1
