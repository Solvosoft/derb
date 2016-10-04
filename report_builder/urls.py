from django.conf.urls import url
from django.conf.urls import include
from report_builder import views
from report_builder.Question.QuestionType import integer_question
from report_builder import initial_views as init
from report_builder.Question.QuestionType import simple_text_question

from report_builder.Question.QuestionType import boolean_question

# Boolean question
# Integer question
# Simple text question
question_types_urls = [
    url(r'boolean/admin$', boolean_question.BooleanQuestionViewAdmin.as_view(),
        name='boolean_question_admin'),
    url(r'boolean/resp/(?P<question_pk>\d+)$', boolean_question.BooleanQuestionViewResp.as_view(),
        name='boolean_question_resp'),
    url(r'boolean/pdf/(?P<question_pk>\d+)$', boolean_question.BooleanQuestionViewPDF.as_view(),
        name='boolean_question_pdf'),
    url(r'integer/admin$', integer_question.IntegerQuestionAdmin.as_view(),
        name='integer_question_admin'),
    url(r'integer/resp/(?P<question_pk>\d+)', integer_question.IntegerQuestionResp.as_view(),
        name='integer_question_resp'),
    url(r'integer/pdf/(?P<question_pk>\d+)', integer_question.IntegerQuestionViewPDF.as_view(),
        name='integer_question_pdf'),
    url(r'simple/admin', simple_text_question.SimpleTextQuestionAdmin.as_view(),
        name='simple_text_question_admin'),
    url(r'simple/resp/(?P<question_pk>\d+)', simple_text_question.SimpleQuestionViewResp.as_view(),
        name='simple_text_question_resp'),
    url(r'simple/pdf/(?P<question_pk>\d+)', simple_text_question.SimpleTextQuestionPDF.as_view(),
        name='simple_text_question_pdf')
]

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^init$', init.InitialIndexView.as_view(), name='init'),
    url(r'^report/new/$', init.NewReportView.as_view(), name='new_report_template'),
    url(r'^question_types/', include(question_types_urls))
]