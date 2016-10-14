from django.conf.urls import url
from django.conf.urls import include
from django.contrib import admin

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^', include('report_builder.urls', namespace='report_builder')),
    url(r'^accounts/', include('registration.backends.hmac.urls')),
    url(r'^password_recovery/', include('password_reset.urls')),
    url(r'^ckeditor/', include('ckeditor_uploader.urls')),
]

# DEPENDENCIES URLS
urlpatterns += [
    #url(r'^ckeditor/', include('ckeditor.urls'))
]