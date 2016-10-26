'''
Created on 15/9/2016
@author: nashyra
'''
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django_ajax.decorators import ajax

from report_builder.Question.QuestionView import QuestionViewAdmin, QuestionViewResp, QuestionViewPDF, QuestionViewReviewer
from report_builder.Question.forms import SimpleTextQuestionForm, SimpleTextAnswerForm


class SimpleTextQuestionViewAdmin(QuestionViewAdmin):
    form_class = SimpleTextQuestionForm
    template_name = 'admin/simple_text_question.html'
    name = 'simple_text_question'
    minimal_representation = {
        'human_readable_name': 'Simple text question',
        'help': 'Allows you to make simple text questions',
        'color': '#330065'
    }


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

            return 0

    return HttpResponse(0)
    
    