'''
Created on 15/9/2016

@author: nashyra
'''
from report_builder.Question.QuestionView import QuestionViewAdmin, QuestionViewResp, QuestionViewPDF
from django.shortcuts import render

class SimpleTextQuestionAdmin(QuestionViewAdmin):
    def get(self, request, *args, **kwargs):
        form = self.get_form(instance=self.question)
        print(form)
        parameters = {
            'form':form,
        }
        return render(request, 'admin/simple_text_question.html', parameters)