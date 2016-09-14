from django.conf.urls import url

from report_builder import views

from report_builder import initial_views as init
from report_builder.Question.QuestionType.unique_selection_question import UniqueSelectionAdmin,\
    UniqueSelectionResp, UniqueSelectionPDF

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^init$', init.InitialIndexView.as_view(), name='init'),
    url(r'^report/new/$', init.NewReportView.as_view(), name='new_report_template')
]


# Unique_Selection_Question
urlpatterns += [
    url(r"^unique_selection_admin$", UniqueSelectionAdmin.as_view(),
        name="unique_selection_admin"),
    url(r"^unique_selection_resp$", UniqueSelectionResp.as_view(),
        name="unique_selection_resp"),
    url(r"^unique_selection_pdf$", UniqueSelectionPDF.as_view(),
        name="unique_selection_pdf"),
]
