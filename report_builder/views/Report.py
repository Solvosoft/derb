import json
from datetime import datetime
from django.shortcuts import get_object_or_404, render

from report_builder.Question.question_loader import process_questions, get_view_type
from django.views.decorators.gzip import gzip_page
from django.contrib.auth.decorators import login_required

from report_builder.forms import AdminReportForm
from report_builder.models import Report


def process_template(request, report, view_type, reportbyproj=None):
    '''
        Loads the questions of the given report, works both for the admin and responsable views

        If ``reportbyproj`` is provided, it also loads the answers of the questions in this report
    '''
    categories = report.template
    i = 0
    for category in categories:
        ii = 0
        for subcategory in category['subcategories']:
            if subcategory['questions']:
                questions = process_questions(request, report.pk, subcategory['questions'], view_type=view_type,
                                              reportbyproj=reportbyproj)
                categories[i]['subcategories'][ii]['questions'] = questions
            ii += 1
        i += 1
    return categories

@gzip_page
@login_required
def admin(request, pk=None):
    '''
        Main administration view for report templates

        Requires the 'template_admin' permission to get access to it. In case the user don't have this permission
        the view renders a page with message explaining the lack of privileges
    '''
    if request.user.has_perm('derb.template_admin'):
        report = None
        if pk:
            report = get_object_or_404(Report, pk=pk)

        if report.opening_date <= datetime.now().date():
            return render(request, 'admin/out_of_date.html')

        admin_views = get_view_type('admin')

        palette = {}

        for name, value in admin_views.items():
            palette[name] = value.minimal_representation

        categories = process_template(request, report, view_type='admin', reportbyproj=None)
        form = AdminReportForm(instance=report)
        context = {
            'report': report,
            'palette': palette,
            'categories': categories,
            'form': form
        }
        return render(request, 'admin/report.html', context=context)
    else:
        return render(request, 'global/permission_denied.html')


@login_required
def save_admin(request, pk):
    '''
        Allows to save the report template in the database
    '''
    if request.method == 'POST':
        if request.user.has_perm('derb.template_admin'):
            report = get_object_or_404(Report, pk=pk)
            old_questions = report.template
            form = AdminReportForm(request.POST, instance=report)

            if form.is_valid():
                rep = report.save(False)
                rep.template = json.loads(form.cleaned_data['template'])
                rep.save()
