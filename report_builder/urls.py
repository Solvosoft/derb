from django.conf.urls import url

from report_builder import views

from report_builder import initial_views as init
from report_builder.Question.QuestionType.unique_selection_question import UniqueSelectionAdmin,\
    UniqueSelectionResp, UniqueSelectionPDF, get_catalog_display_fields

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^init$', init.InitialIndexView.as_view(), name='init'),
    url(r'^report/new/$', init.NewReportView.as_view(), name='new_report_template')
]


# Unique_Selection_Question
urlpatterns += [
    url(r"^unique/admin$", UniqueSelectionAdmin.as_view(),
        name="unique_selection_admin"),
    url(r"^unique/resp/(?P<question_pk>\d+)", UniqueSelectionResp.as_view(),
        name="unique_selection_resp"),
    url(r"^unique/pdf/(?P<question_pk>\d+)", UniqueSelectionPDF.as_view(),
        name="unique_selection_pdf"),
    url(r"^get_catalog_display_fields", get_catalog_display_fields, 
        name='get_catalog_display_fields')
]
