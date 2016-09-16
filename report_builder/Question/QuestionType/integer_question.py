'''
Created on 14/9/2016

@author: natalia
'''
from report_builder.Question.QuestionView import QuestionViewAdmin, QuestionViewResp, QuestionViewPDF
from django.shortcuts import render

class IntegerQuestionAdmin(QuestionViewAdmin):
    def get(self, request, *args, **kwargs):
        return render(request, 'admin/integer_question.html')