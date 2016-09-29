from django.conf.urls import url

from report_builder import views

from report_builder import initial_views as init

from report_builder.Question.QuestionType import simple_text_question

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^init$', init.InitialIndexView.as_view(), name='init'),
    url(r'^report/new/$', init.NewReportView.as_view(), name='new_report_template'),
]

# Question types
urlpatterns += [
    url(r'^question_type/simple/admin', simple_text_question.SimpleTextQuestionAdmin.as_view(),
        name='simple_text_question_admin'),
    url(r'^question_type/simple/resp/(?P<question_pk>\d+)', simple_text_question.SimpleQuestionViewResp.as_view(),
        name='simple_text_question_resp'),
    url(r'^question_type/simple/pdf/(?P<question_pk>\d+)', simple_text_question.SimpleTextQuestionPDF.as_view(),
        name='simple_text_question_pdf')
]
