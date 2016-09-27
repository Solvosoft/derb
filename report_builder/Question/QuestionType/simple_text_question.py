'''
Created on 15/9/2016

@author: nashyra
'''
from report_builder.Question.QuestionView import QuestionViewAdmin, QuestionViewResp, QuestionViewPDF
from django.shortcuts import render
from report_builder.Question.forms import SimpleTextQuestionForm, SimpleTextResp
from django.http import HttpResponse


class SimpleTextQuestionAdmin(QuestionViewAdmin):
    form_class = SimpleTextQuestionForm

    def get(self, request, *args, **kwargs):
        form = self.get_form()
        parameters = {
            'form': form,
        }
        return render(request, 'admin/simple_text_question.html', parameters)
    
    def post(self, request, *args, **kwargs):
        form = self.get_form(request.POST, instance=self.question)
        if form.is_valid():
            question = form.save(False)
            question.report = self.report
            question.class_to_load = self.name
            question = self.pre_save(question, request, form)
            question.save()

        return HttpResponse(str(question.pk))
    

class SimpleTextQuestionResp(QuestionViewResp):
    form_class = SimpleTextResp
    def get(self, request, *args, **kwargs):
        return render(request, 'responsable/simple_text_question.html')


class SimpleTextQuestionPDF(QuestionViewPDF):
    def get(self, request, *args, **kwargs):
        return render(request, 'pdf/simple_text_question.html')