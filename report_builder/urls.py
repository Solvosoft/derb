from django.conf.urls import include
from django.conf.urls import url

from report_builder import initial_views as init
from report_builder import views
from report_builder.Question import QuestionView
from report_builder.Question.QuestionType import (table_question,
                                                  simple_text_question,
                                                  multiple_selection_question,
                                                  boolean_question,
                                                  integer_question,
                                                  float_question,
                                                  unique_selection_question,
                                                  model_info,
                                                  question_model_info)
from report_builder.Question.QuestionType.simple_text_question import submit_new_observation
from report_builder.Question.QuestionType.unique_selection_question import get_catalog_display_fields
from report_builder.Question.question_loader import process_question
from report_builder.views import Report

# Boolean question
# Integer question
# Float question
# Simple text question
# Unique selection question
# Multiple selection question
# Model info
# Model info with questions
question_types_urls = [
    url(r'base/admin/(?P<report_pk>\d+)/(?P<question_pk>\d+)?$', QuestionView.QuestionViewAdmin.as_view(),
        name='base_question_admin'),
    url(r'base/resp/(?P<report_pk>\d+)/(?P<question_pk>\d+)$', QuestionView.QuestionViewResp.as_view(),
        name='base_question_resp'),
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
    url(r'integer/admin/(?P<report_pk>\d+)/(?P<question_pk>\d+)?$', integer_question.IntegerQuestionViewAdmin.as_view(),
        name='integer_question_admin'),
    url(r'integer/resp/(?P<report_pk>\d+)/(?P<question_pk>\d+)$', integer_question.IntegerQuestionViewResp.as_view(),
        name='integer_question_resp'),
    url(r'integer/pdf/(?P<report_pk>\d+)/(?P<question_pk>\d+)', integer_question.IntegerQuestionViewPDF.as_view(),
        name='integer_question_pdf'),
    url(r'integer/revisor/(?P<report_pk>\d+)/(?P<question_pk>\d+)',
        integer_question.IntegerQuestionViewReviewer.as_view(),
        name='integer_question_revisor'),
    url(r'integer/csv/(?P<report_pk>\d+)/(?P<question_pk>\d+)$',
        integer_question.IntegerQuestionViewCSV.as_view(),
        name='integer_question_csv'),
    url(r'integer/json/(?P<report_pk>\d+)/(?P<question_pk>\d+)$',
        integer_question.IntegerQuestionViewJSON.as_view(),
        name='integer_question_json'),
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
    url(r'simple/revisor/(?P<report_pk>\d+)/(?P<question_pk>\d+)',
        simple_text_question.SimpleTextQuestionViewReviewer.as_view(),
        name='simple_text_question_revisor'),
    url(r'simple/csv/(?P<report_pk>\d+)/(?P<question_pk>\d+)$', simple_text_question.SimpleQuestionViewCSV.as_view(),
        name='simple_text_question_csv'),
    url(r'simple/json/(?P<report_pk>\d+)/(?P<question_pk>\d+)$', simple_text_question.SimpleQuestionViewJSON.as_view(),
        name='simple_text_question_json'),
    url(r"unique/admin/(?P<report_pk>\d+)/(?P<question_pk>\d+)?$",
        unique_selection_question.UniqueSelectionQuestionViewAdmin.as_view(),
        name="unique_selection_admin"),
    url(r"unique/resp/(?P<report_pk>\d+)/(?P<question_pk>\d+)$",
        unique_selection_question.UniqueSelectionQuestionViewResp.as_view(),
        name="unique_selection_resp"),
    url(r"unique/pdf/(?P<report_pk>\d+)/(?P<question_pk>\d+)",
        unique_selection_question.UniqueSelectionQuestionViewPDF.as_view(),
        name="unique_selection_pdf"),
    url(r'unique/revisor/(?P<report_pk>\d+)/(?P<question_pk>\d+)',
        unique_selection_question.UniqueSelectionQuestionViewReviewer.as_view(),
        name='unique_selection_question_revisor'),
    url(r'unique/csv/(?P<report_pk>\d+)/(?P<question_pk>\d+)$',
        unique_selection_question.UniqueQuestionViewCSV.as_view(),
        name='unique_selection_csv'),
    url(r'unique/json/(?P<report_pk>\d+)/(?P<question_pk>\d+)$',
        unique_selection_question.UniqueQuestionViewJSON.as_view(),
        name='unique_selection_json'),
    url(r"table/admin/(?P<report_pk>\d+)/(?P<question_pk>\d+)?$",
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
    url(r"multiple/admin/(?P<report_pk>\d+)/(?P<question_pk>\d+)?$",
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
        name='multiple_selection_question_json'),
    url(r'model_info/admin/(?P<report_pk>\d+)/(?P<question_pk>\d+)?', model_info.ModelInfoViewAdmin.as_view(),
        name='model_info_question'),
    url(r'question_model_info/admin/(?P<report_pk>\d+)/(?P<question_pk>\d+)?',
        question_model_info.QuestionModelInfoViewAdmin.as_view(), name='question_model_info_question')
]

# Report views
report_views_urls = [
    url(r'^new/$', init.NewReportView.as_view(), name='new_report'),
    url(r'^new/(?P<pk>\d+)$', init.NewReportTemplate,
        name='new_report_from_template'),
    url(r'^admin/template/(?P<pk>\d+)$', Report.admin, name='admin_report'),
    url(r'^admin/template/(?P<pk>\d+)/save$',
        Report.save_admin, name='admin_save_report'),
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
    url(r'^js/ckeditor_config.js', views.get_js_editor,
        name='js_ckeditor_config'),
    url(r'^init$', init.InitialIndexView.as_view(), name='init'),
    url(r'^question_types/', include(question_types_urls)),
    url(r'^report/', include(report_views_urls)),
    url(r'^question_processing/', include(question_process_urls)),
    url(r"^get_catalog_display_fields", get_catalog_display_fields,
        name='get_catalog_display_fields'),
    url(r"^submit_new_observation$", submit_new_observation,
        name='submit_new_observation')
]