'''
Created on 15/9/2016

@author: nashyra
'''
from django.http import HttpResponse
from django.views.generic.edit import CreateView
from django.views.generic.list import ListView
from django.utils import timezone

from report_builder.Question.QuestionView import QuestionViewAdmin, QuestionViewResp, QuestionViewPDF


class miContexto(object):

    def get_context_data(self, **kwargs):
        contex = ListView.get_context_data(self, **kwargs)
        contex['datetime'] = timezone.now()
        return contex

class SimpleTextAdmin(QuestionViewAdmin):
    def hola(self):
        return print("hola")
       
class SimpleTextResp(QuestionViewResp):
    def hola(self):
        return print("hola")
        
class SimpleTextPDF(QuestionViewPDF):
    def hola(self):
        return print("hola")