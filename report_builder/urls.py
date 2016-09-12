from django.conf.urls import url
from report_builder import views
from report_builder.initial_views import InitialIndexView

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^init$', InitialIndexView.as_view(), name='init')
]