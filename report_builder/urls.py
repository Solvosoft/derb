from django.conf.urls import url
from report_builder import views
from report_builder import initial_views as init
from report_builder.views import Report

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^js/ckeditor_config.js', views.get_js_editor, name='js_ckeditor_config'),
    url(r'^init$', init.InitialIndexView.as_view(), name='init'),
    url(r'^report/new/$', init.NewReportView.as_view(), name='new_report'),
    url(r'^report/new/(?P<pk>\d+)$', init.NewReportTemplate, name='new_report_from_template')
]

# Report views
urlpatterns += [
    url(r'^admin/template/(?P<pk>\d+)$', Report.admin, name='admin_report'),
    url(r'^admin/template/(?P<pk>\d+)/save$', Report.save_admin, name='admin_save_report')
]