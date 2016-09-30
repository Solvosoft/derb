from django.conf.urls import url

from report_builder import views
from report_builder.Question.QuestionType import integer_question
from report_builder import initial_views as init

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^init$', init.InitialIndexView.as_view(), name='init'),
    url(r'^report/new/$', init.NewReportView.as_view(), name='new_report_template')
]

# Question types

#Integer Question
urlpatterns += [
    url(r'^integer_question_admin', integer_question.IntegerQuestionAdmin.as_view(), 
        name='integer_question_admin'),
    url(r'^integer_question_responsable/(?P<question_pk>\d+)', integer_question.IntegerQuestionResp.as_view(),
        name='integer_question_resp'),
    url(r'^integer_question/pdf/(?P<question_pk>\d+)', integer_question.IntegerQuestionViewPDF.as_view(),
        name='integer_question_pdf')
]
