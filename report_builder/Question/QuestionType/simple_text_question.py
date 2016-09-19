'''
Created on 15/9/2016

@author: nashyra
'''
from report_builder.Question.QuestionView import QuestionViewAdmin
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
