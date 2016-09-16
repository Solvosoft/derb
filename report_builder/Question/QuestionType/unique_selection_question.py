'''
Created on 14/9/2016

@author: adolfo
'''

from django.shortcuts import render
from report_builder.Question import QuestionView

class UniqueSelectionAdmin(QuestionView.QuestionViewAdmin):
    def get(self, request, *args, **kwargs):
        return render(request, 'admin/unique_selection_question.html')
       
class UniqueSelectionResp(QuestionView.QuestionViewResp):
    def get(self, request, *args, **kwargs):
        return render(request, 'responsable/unique_selection_question.html')
        
class UniqueSelectionPDF(QuestionView.QuestionViewPDF):
    def get(self, request, *args, **kwargs):
        return render(request, 'pdf/unique_selection_question.html')
