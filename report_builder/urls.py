from django.conf.urls import url

from report_builder import views

from report_builder import initial_views as init

from report_builder.Question.QuestionType import boolean_question

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^init$', init.InitialIndexView.as_view(), name='init'),
    url(r'^report/new/$', init.NewReportView.as_view(), name='new_report_template')
]

# Question types
urlpatterns += [
    url(r'^question_types/boolean/admin', boolean_question.BooleanQuestionViewAdmin.as_view(), name='boolean_question_admin')
]