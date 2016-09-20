'''
Created on 14/9/2016

@author: adolfo
'''

from django.shortcuts import render
from report_builder.Question import QuestionView
from report_builder.Question.forms import QuestionForm, AnswerForm

class UniqueSelectionAdmin(QuestionView.QuestionViewAdmin, QuestionForm):
    def get(self, request, *args, **kwargs):
        return render(request, 'admin/unique_selection_question.html')
       
class UniqueSelectionResp(QuestionView.QuestionViewResp, AnswerForm):
    def get(self, request, *args, **kwargs):
        return render(request, 'responsable/unique_selection_question.html')
        
class UniqueSelectionPDF(QuestionView.QuestionViewPDF):
    def get(self, request, *args, **kwargs):
        return render(request, 'pdf/unique_selection_question.html')
