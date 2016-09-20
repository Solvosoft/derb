'''
Created on 14/9/2016

@author: adolfo
'''

from django.shortcuts import render
from report_builder.Question import QuestionView
from report_builder.Question.forms import UniqueSelectionForm

class UniqueSelectionAdmin(QuestionView.QuestionViewAdmin):
    form_class = UniqueSelectionForm
    
    def get(self, request, *args, **kwargs):
        form = self.get_form()
        parameters = {
                      "form": form, 
        }
        return render(request, 'admin/unique_selection_question.html', parameters)
       
class UniqueSelectionResp(QuestionView.QuestionViewResp):
    def get(self, request, *args, **kwargs):
        return render(request, 'responsable/unique_selection_question.html')
        
class UniqueSelectionPDF(QuestionView.QuestionViewPDF):
    def get(self, request, *args, **kwargs):
        return render(request, 'pdf/unique_selection_question.html')
