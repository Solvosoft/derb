from django.conf.urls import url
from report_builder import views

urlpatterns = [
    url('^$', views.index, name='index')
]