'''
Created on 15/9/2016
@author: nashyra
'''
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django_ajax.decorators import ajax
from django.template.loader import render_to_string

from report_builder.Question.QuestionView import QuestionViewAdmin, QuestionViewResp, QuestionViewPDF, QuestionViewReviewer, QuestionViewCSV,QuestionViewJSON
from report_builder.Question.forms import SimpleTextQuestionForm, SimpleTextAnswerForm
from report_builder.models import Question
from report_builder.models import Answer, Observation, Reviewer


class SimpleTextQuestionViewAdmin(QuestionViewAdmin):
    '''
        SimpleTextQuestionViewAdmin class represents the implementation of the template administrator view for a question object
        This view is built to be extended from the different question types of the Derb system
        By itself, this view provides the functionality for ordering and deletion of question, and a form with question
        text and help
        
        This class be extended using an implementation like this:

        .. code:: python

            from report_builder.Question.QuestionView import QuestionViewAdmin
            class MyQuestion(QuestionViewAdmin):
                template_name = 'path/to/the/template'
                name = 'my_question'

        The extended methods can be overridden to adjust the functionality of the extended class. For instance:

        .. code:: python

            def additional_template_parameters(self, **kwargs):
                some_dict = {
                    'something': some_variable
                }
                return some_dict

        .. note::
            *kwargs* is a dict that contains the Question attributes 'form', 'report', 'question' and 'name'
            You don't have to append the kwargs content in the return value, only the additional elements
    '''
    form_class = SimpleTextQuestionForm #: Default form for the class
    template_name = 'admin/question_types/simple_text_question.html' #: Specifies which template to load
    name = 'simple_text_question' #: Class reference name
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
        object.answer_options = repr(form.cleaned_data['on_modal'])
        object.required = Question.OPTIONAL
        return object

    def additional_template_parameters(self, **kwargs):
        return {}


# class SimpleTextQuestionResp(QuestionViewResp):
class SimpleQuestionViewResp(QuestionViewResp):
    """
        SimpleQuestionViewResp class represents the implementation of the template administrator view for a question object
        This view is built to be extended from the different question types of the Derb system
        By itself, this view shows the simple question created by the template administrator, including the question text and help
        set by the user. Additionally, it provides a form two fields, a text area for the user to answer the question and a text area
        to add annotations for the reviewers. Plus, when a reviewer user has applied observations to the question, it shows such observations.

        .. note::
            * Extends from the Question class, so if you want to take a look to the extended methods and attributes,
            you can find it in :mod:`report_builder.Question.QuestionView.Question`
    """
    name = 'simple_text_question' #: Class reference name
    template_name = 'responsable/simple_text_question.html' #: Specifies which template to load
    form_class = SimpleTextAnswerForm #: Default form for the class


# class SimpleTextQuestionPDF(QuestionViewPDF):
class SimpleTextQuestionViewPDF(QuestionViewPDF):
    """
        SimpleTextQuestionViewPDF class represents the implementation of exporting a question object to a PDF document
        This view is built to be extended from the different question types of the Derb system
        By itself, this view saves in the PDF the simple question created by the template administrator, including
        the question text and help set by the user. Additionally, if a responsable user has answered the question,
        it shows the answer text and annotations provided. Finally, if one or more reviewer users applied
        observations to the question, it shows such observations.

        .. note::
            * Extends from the Question class, so if you want to take a look to the extended methods and attributes,
            you can find it in :mod:`report_builder.Question.QuestionView.Question`
    """
    name = 'simple_text_question' #: Class reference name
    template_name = 'pdf/simple_text_question.html' #: Specifies which template to load
    

class SimpleTextQuestionViewReviewer(QuestionViewReviewer):
    """
        SimpleTextQuestionViewReviewer class represents the implementation of the reviewer view for a question object
        This view is built to be extended from the different question types of the Derb system
        By itself, this view shows the simple question created by the template administrator, including
        the question text and help set by the user. Additionally, if a responsable user has answered the question,
        it shows the answer text and annotations provided. Finally, if one or more reviewer users applied
        observations to the question, it shows such observations.

        .. note::
            * Extends from the Question class, so if you want to take a look to the extended methods and attributes,
            you can find it in :mod:`report_builder.Question.QuestionView.Question`
    """
    name = 'simple_text_question' #: Class reference name
    template_name = 'revisor/simple_text_question.html' #: Specifies which template to load
    

@ajax
@csrf_exempt
def submit_new_observation(request):
    """
            Handles the requests using the *GET* HTTP verb triggered by a user to save an observation and refresh the page using ajax code
            The context passed to the template contains (at least) the next elements:
               - question
               - question_number
               - answer
               - observations
               - report number
    """

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
    """
        SimpleQuestionViewCSV class represents the implementation of exporting a question object to a CSV formatted string
        This view is built to be extended from the different question types of the Derb system
        By itself, this view saves in the CSV string the simple question created by the template administrator, including
        the question text and help set by the user. Additionally, if a responsable user has answered the question,
        it saves the answer text and annotations provided. Finally, if one or more reviewer users applied
        observations to the question, it saves such observations.

        .. note::
            * Extends from the Question class, so if you want to take a look to the extended methods and attributes,
            you can find it in :mod:`report_builder.Question.QuestionView.Question`
    """
    name = 'simple_text_question' #: Class reference name
    

class SimpleQuestionViewJSON(QuestionViewJSON):
    """
        SimpleQuestionViewJSON class represents the implementation of exporting a question object to a JSON formatted string
        This view is built to be extended from the different question types of the Derb system
        By itself, this view saves in the JSON string the simple question created by the template administrator, including
        the question text and help set by the user. Additionally, if a responsable user has answered the question,
        it saves the answer text and annotations provided. Finally, if one or more reviewer users applied
        observations to the question, it saves such observations.

        .. note::
            * Extends from the Question class, so if you want to take a look to the extended methods and attributes,
            you can find it in :mod:`report_builder.Question.QuestionView.Question`
    """
    name = 'simple_text_question' #: Class reference name
    
