import json
from django.http.response import HttpResponse
from django.shortcuts import render, redirect
from django.conf import settings
from django.urls import reverse


def index(request):
    if request.user.is_authenticated():
        return redirect(reverse('report_builder:init'))
    else:
        return render(request, 'derb/index.html')


def get_js_editor(request):
    '''
    Retrieves the ckedit settings saved in the web interface and returns them as an HTTP response
    to be accesed and edited
    '''
    response = 'ckeditor_conf=%s' % json.dumps(settings.CKEDITOR_CONFIGS)
    return HttpResponse(response)