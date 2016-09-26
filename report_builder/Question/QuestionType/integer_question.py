'''
Created on 14/9/2016

@author: natalia
'''
from report_builder.Question.QuestionView import QuestionViewAdmin, QuestionViewResp, QuestionViewPDF
from django.shortcuts import render
from report_builder.Question.forms import IntegerQuestionForm, AnswerForm



class IntegerQuestionAdmin(QuestionViewAdmin):
    form_class=  IntegerQuestionForm

    def get(self, request, *args, **kwargs):
        form = self.get_form(instance=self.question)
        print(form)
        parameters = {
            'form': form,
         }
        return render(request,'admin/integer_question.html', parameters)

class IntegerQuestionResp(QuestionViewResp):
    form_class = AnswerForm
    def get(self, request, *args, **kwargs):
        form = self.get_form(instance=self.question)
        print(form)
        parameters = {
            'form': form,
         }
        return render(request, 'responsable/integer_question.html',parameters)
        
