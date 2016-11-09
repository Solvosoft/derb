from django.conf.urls import url
from django.conf.urls import include

from report_builder import views
from report_builder import initial_views as init
from report_builder.Question.question_loader import process_question
from report_builder.Question import QuestionView
from report_builder.Question.QuestionType import table_question
from report_builder.Question.QuestionType import simple_text_question
from report_builder.Question.QuestionType import multiple_selection_question
from report_builder.Question.QuestionType import boolean_question
from report_builder.Question.QuestionType import integer_question
from report_builder.Question.QuestionType import float_question
from report_builder.Question.QuestionType import unique_selection_question
from report_builder.Question.QuestionType.unique_selection_question import get_catalog_display_fields
from report_builder.views import Report

# Boolean question
# Integer question
# Float question
# Simple text question
# Unique selection question
# Multiple selection question
question_types_urls = [
    url(r'base/admin/(?P<report_pk>\d+)/(?P<question_pk>\d+)?$', QuestionView.QuestionViewAdmin.as_view(),
        name='base_question_admin'),
    url(r'boolean/admin/(?P<report_pk>\d+)/(?P<question_pk>\d+)?$', boolean_question.BooleanQuestionViewAdmin.as_view(),
        name='boolean_question_admin'),
    url(r'boolean/resp/(?P<report_pk>\d+)/(?P<question_pk>\d+)$', boolean_question.BooleanQuestionViewResp.as_view(),
        name='boolean_question_resp'),
    url(r'boolean/pdf/(?P<report_pk>\d+)/(?P<question_pk>\d+)$', boolean_question.BooleanQuestionViewPDF.as_view(),
        name='boolean_question_pdf'),
    url(r'boolean/revisor/(?P<report_pk>\d+)/(?P<question_pk>\d+)$',
        boolean_question.BooleanQuestionViewReviewer.as_view(),
        name='boolean_question_revisor'),
    url(r'boolean/csv/(?P<report_pk>\d+)/(?P<question_pk>\d+)$', boolean_question.BooleanQuestionViewCSV.as_view(),
        name='boolean_question_csv'),
    url(r'boolean/json/(?P<report_pk>\d+)/(?P<question_pk>\d+)$', boolean_question.BooleanQuestionViewJSON.as_view(),
        name='boolean_question_json'),
    url(r'boolean/spss/(?P<report_pk>\d+)/(?P<question_pk>\d+)$', boolean_question.BooleanQuestionViewSPSS.as_view(),
        name='boolean_question_spss'),
    url(r'integer/admin/(?P<report_pk>\d+)/(?P<question_pk>\d*)$', integer_question.IntegerQuestionViewAdmin.as_view(),
        name='integer_question_admin'),
    url(r'integer/resp/(?P<report_pk>\d+)/(?P<question_pk>\d+)$', integer_question.IntegerQuestionViewResp.as_view(),
        name='integer_question_resp'),
    url(r'integer/pdf/(?P<report_pk>\d+)/(?P<question_pk>\d+)', integer_question.IntegerQuestionViewPDF.as_view(),
        name='integer_question_pdf'),
    url(r'float/admin/(?P<report_pk>\d+)/(?P<question_pk>\d+)?$', float_question.FloatQuestionViewAdmin.as_view(),
        name='float_question_admin'),
    url(r'float/resp/(?P<report_pk>\d+)/(?P<question_pk>\d+)$', float_question.FloatQuestionViewResp.as_view(),
        name='float_question_resp'),
    url(r'float/pdf/(?P<report_pk>\d+)/(?P<question_pk>\d+)', float_question.FloatQuestionViewPDF.as_view(),
        name='float_question_pdf'),
    url(r'simple/admin/(?P<report_pk>\d+)/(?P<question_pk>\d+)?$',
        simple_text_question.SimpleTextQuestionViewAdmin.as_view(),
        name='simple_text_question_admin'),
    url(r'simple/resp/(?P<report_pk>\d+)/(?P<question_pk>\d+)$', simple_text_question.SimpleQuestionViewResp.as_view(),
        name='simple_text_question_resp'),
    url(r'simple/pdf/(?P<report_pk>\d+)/(?P<question_pk>\d+)', simple_text_question.SimpleTextQuestionViewPDF.as_view(),
        name='simple_text_question_pdf'),
    url(r"unique/admin/(?P<report_pk>\d+)/(?P<question_pk>\d*)$",
        unique_selection_question.UniqueSelectionQuestionViewAdmin.as_view(),
        name="unique_selection_admin"),
    url(r"unique/resp/(?P<report_pk>\d+)/(?P<question_pk>\d+)$",
        unique_selection_question.UniqueSelectionQuestionViewResp.as_view(),
        name="unique_selection_resp"),
    url(r"unique/pdf/(?P<report_pk>\d+)/(?P<question_pk>\d+)",
        unique_selection_question.UniqueSelectionQuestionViewPDF.as_view(),
        name="unique_selection_pdf"),
    url(r"table/admin/(?P<report_pk>\d+)/(?P<question_pk>\d*)$",
        table_question.TableQuestionViewAdmin.as_view(),
        name="table_question_admin"),
    url(r"table/resp/(?P<report_pk>\d+)/(?P<question_pk>\d+)$",
        table_question.TableQuestionViewResp.as_view(),
        name="table_question_resp"),
    url(r"table/pdf/(?P<report_pk>\d+)/(?P<question_pk>\d+)",
        table_question.TableQuestionViewPDF.as_view(),
        name="table_question_pdf"),
    url(r'table/csv/(?P<report_pk>\d+)/(?P<question_pk>\d+)$',
        table_question.TableQuestionViewCSV.as_view(),
        name='table_question_csv'),
    url(r'table/json/(?P<report_pk>\d+)/(?P<question_pk>\d+)$',
        table_question.TableQuestionViewJSON.as_view(),
        name='table_question_json'),
    url(r"multiple/admin/(?P<report_pk>\d+)/(?P<question_pk>\d*)$",
        multiple_selection_question.MultipleSelectionQuestionViewAdmin.as_view(),
        name="multiple_selection_admin"),
    url(r"multiple/resp/(?P<report_pk>\d+)/(?P<question_pk>\d+)$",
        multiple_selection_question.MultipleSelectionQuestionViewResp.as_view(),
        name="multiple_selection_resp"),
    url(r'multiple/pdf/(?P<report_pk>\d+)/(?P<question_pk>\d+)$',
        multiple_selection_question.MultipleSelectionQuestionViewPDF.as_view(),
        name='multiple_seletion_question_pdf'),
    url(r'multiple/csv/(?P<report_pk>\d+)/(?P<question_pk>\d+)$',
        multiple_selection_question.MultipleSelectionQuestionViewCSV.as_view(),
        name='multiple_selection_question_csv'),
    url(r'multiple/json/(?P<report_pk>\d+)/(?P<question_pk>\d+)$',
        multiple_selection_question.MultipleSelectionQuestionViewJSON.as_view(),
        name='multiple_selection_question_json')
]

# Report views
report_views_urls = [
    url(r'^new/$', init.NewReportView.as_view(), name='new_report'),
    url(r'^new/(?P<pk>\d+)$', init.NewReportTemplate, name='new_report_from_template'),
    url(r'^admin/template/(?P<pk>\d+)$', Report.admin, name='admin_report'),
    url(r'^admin/template/(?P<pk>\d+)/save$', Report.save_admin, name='admin_save_report'),
]

# Question processing
question_process_urls = [
    url(r'(?P<type>admin)/(?P<view_type>\w+)/(?P<report_pk>\d+)/(?P<question_pk>\d+)?$', process_question,
        name='process_admin'),
    url(r'(?P<type>responsable)/(?P<view_type>\w+)/(?P<report_pk>\d+)/(?P<question_pk>\d+)/(?P<answer_pk>\d+)?$',
        process_question, name='process_responsable'),
    url(r'(?P<type>revisor)/(?P<view_type>\w+)/(?P<report_pk>\d+)/(?P<question_pk>\d+)/(?P<answer_pk>\d+)?$',
        process_question, name='process_revisor')
]

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^js/ckeditor_config.js', views.get_js_editor, name='js_ckeditor_config'),
    url(r'^init$', init.InitialIndexView.as_view(), name='init'),
    url(r'^question_types/', include(question_types_urls)),
    url(r'^report/', include(report_views_urls)),
    url(r'^question_processing/', include(question_process_urls)),
    url(r"^get_catalog_display_fields", get_catalog_display_fields, name='get_catalog_display_fields')
]
