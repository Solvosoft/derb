from django.conf.urls import url

from report_builder import views

from report_builder import initial_views as init

from report_builder.Question.QuestionType import simple_text_question

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^init$', init.InitialIndexView.as_view(), name='init'),
    url(r'^report/new/$', init.NewReportView.as_view(), name='new_report_template')
]

# Question types
urlpatterns += [
    url(r'^simple_text_question_admin',simple_text_question.SimpleTextQuestionAdmin.as_view(), name='simple_text_question_admin')
]