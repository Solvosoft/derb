from django.conf.urls import url
from django.conf.urls import include

from report_builder import views
from report_builder import initial_views as init
from report_builder.Question.QuestionType import simple_text_question
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
question_types_urls = [
    url(r'boolean/admin/(?P<report_pk>\d+)/(?P<question_pk>\d*)$', boolean_question.BooleanQuestionViewAdmin.as_view(),
        name='boolean_question_admin'),
    url(r'boolean/resp/(?P<report_pk>\d+)/(?P<question_pk>\d+)$', boolean_question.BooleanQuestionViewResp.as_view(),
        name='boolean_question_resp'),
    url(r'boolean/pdf/(?P<report_pk>\d+)/(?P<question_pk>\d+)$', boolean_question.BooleanQuestionViewPDF.as_view(),
        name='boolean_question_pdf'),
    url(r'boolean/revisor/(?P<report_pk>\d+)/(?P<question_pk>\d+)$',
        boolean_question.BooleanQuestionViewReviewer.as_view(),
        name='boolean_question_revisor'),
    url(r'integer/admin/(?P<report_pk>\d+)/(?P<question_pk>\d*)$', integer_question.IntegerQuestionViewAdmin.as_view(),
        name='integer_question_admin'),
    url(r'integer/resp/(?P<report_pk>\d+)/(?P<question_pk>\d+)$', integer_question.IntegerQuestionViewResp.as_view(),
        name='integer_question_resp'),
    url(r'integer/pdf/(?P<report_pk>\d+)/(?P<question_pk>\d+)', integer_question.IntegerQuestionViewPDF.as_view(),
        name='integer_question_pdf'),
    url(r'float/admin/(?P<report_pk>\d+)/(?P<question_pk>\d*)$', float_question.FloatQuestionViewAdmin.as_view(),
        name='float_question_admin'),
    url(r'float/resp/(?P<report_pk>\d+)/(?P<question_pk>\d+)$', float_question.FloatQuestionViewResp.as_view(),
        name='float_question_resp'),
    url(r'float/pdf/(?P<report_pk>\d+)/(?P<question_pk>\d+)', float_question.FloatQuestionViewPDF.as_view(),
        name='float_question_pdf'),
    url(r'simple/admin/(?P<report_pk>\d+)/(?P<question_pk>\d*)$',
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
]

# Report views
report_views_urls = [
    url(r'^new/$', init.NewReportView.as_view(), name='new_report'),
    url(r'^new/(?P<pk>\d+)$', init.NewReportTemplate, name='new_report_from_template'),
    url(r'^admin/template/(?P<pk>\d+)$', Report.admin, name='admin_report'),
    url(r'^admin/template/(?P<pk>\d+)/save$', Report.save_admin, name='admin_save_report'),
]

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^js/ckeditor_config.js', views.get_js_editor, name='js_ckeditor_config'),
    url(r'^init$', init.InitialIndexView.as_view(), name='init'),
    url(r'^question_types/', include(question_types_urls)),
    url(r'^report/', include(report_views_urls)),
    url(r"^get_catalog_display_fields", get_catalog_display_fields, name='get_catalog_display_fields')
]