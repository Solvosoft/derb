from django.conf.urls import include
from django.conf.urls import url
from django.contrib import admin
from django.conf import settings

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^',
        include('report_builder.urls', namespace='report_builder')),
    url(r'^accounts/', include('registration.backends.hmac.urls')),
    url(r'^password_recovery/', include('password_reset.urls')),
    url(r'^ckeditor/', include('ckeditor_uploader.urls')),
]

# DEPENDENCIES URLS
urlpatterns += [
    #url(r'^ckeditor/', include('ckeditor.urls'))
]


if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        url(r'^__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns
