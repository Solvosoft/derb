'''
Created on 15/9/2016

@author: nashyra
'''
from report_builder.Question.QuestionView import QuestionViewAdmin, QuestionViewResp, QuestionViewPDF
from django.shortcuts import render
from report_builder.Question.forms import SimpleTextQuestionForm


class SimpleTextQuestionAdmin(QuestionViewAdmin):
    form_class = SimpleTextQuestionForm

    def get(self, request, *args, **kwargs):
        form = self.get_form()
        parameters = {
            'form': form,
        }
        return render(request, 'admin/simple_text_question.html', parameters)
    

class SimpleTextQuestionResp(QuestionViewResp):
    def get(self, request, *args, **kwargs):
        return render(request, 'responsable/simple_text_question.html')


class SimpleTextQuestionPDF(QuestionViewPDF):
    def get(self, request, *args, **kwargs):
        return render(request, 'pdf/simple_text_question.html')