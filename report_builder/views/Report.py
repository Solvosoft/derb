import json
from django.http import HttpResponse

from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.utils import timezone
from django.views.decorators.http import require_POST

from report_builder.Project_Wrapper import is_responsable_of_project
from report_builder.Question.question_loader import get_view_type, \
    process_questions
from report_builder.forms import AdminReportForm
from report_builder.models import RS_EDITING, RS_SUBMIT_PENDING, Report, \
    ReportByProject
from report_builder.report_shortcuts import build_report_object_with_thread, \
    delete_questions_with_thread


def process_template(request, report, view_type, reportbyproj=None):
    '''
        Loads the questions of the given report, works both for the admin and 
        responsable views

        If ``reportbyproj`` is provided, it also loads the answers of the 
        questions in this report
    '''
    categories = report.template
    i = 0
    for category in categories:
        ii = 0
        for subcategory in category['subcategories']:
            if subcategory['questions']:
                questions = process_questions(
                    request, report.pk, subcategory['questions'],
                    view_type=view_type, reportbyproj=reportbyproj)
                categories[i]['subcategories'][ii]['questions'] = questions
            ii += 1
        i += 1
    return categories


@login_required
def admin(request, pk=None):
    '''
        Main administration view for report templates

        Requires the 'template_admin' permission to get access to it. 
        In case the user don't have this permission the view renders a 
        page with message explaining the lack of privileges
    '''
    if request.user.has_perm('derb.template_admin'):
        report = None
        if pk:
            report = get_object_or_404(Report, pk=pk)

        if report.opening_date <= timezone.now():
            return render(request, 'admin/out_of_date.html')

        admin_views = get_view_type('admin')

        palette = {}

        for name, value in admin_views.items():
            palette[name] = value.minimal_representation

        categories = process_template(
            request, report, view_type='admin', reportbyproj=None)

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


@require_POST
@login_required
def save_admin(request, pk):
    '''
        Allows to save the report template in the database
    '''

    if request.user.has_perm('derb.template_admin'):
        report = get_object_or_404(Report, pk=pk)
        old_questions = report.template
        form = AdminReportForm(request.POST, instance=report)
        if form.is_valid():
            rep = form.save(False)
            rep.template = json.loads(form.cleaned_data['template'])
            rep.save()

            delete_questions_with_thread(old_questions, rep.template)
            build_report_object_with_thread(rep)

            return HttpResponse('1')
        else:
            return render(request, 'admin/report_form.html',
                          {'form': form,  'report': report})


@login_required
def responsable(request, pk):
    '''
    Vista principal del informe para usuarios responsables de proyectos.

    Revisa que el usuario posea los permisos para acceder a esta vista, de no ser así se
    renderiza una plantilla con un mensaje indicando la falta de permisos.
    Si el informe aún no está vigente se renderiza una plantilla indicando el error y mostrando
    la fecha de inicio del informe.

    '''
    reportbyproj = get_object_or_404(ReportByProject, pk=pk)

    # request.user.has_perm('derb.template_admin')
    if not is_responsable_of_project(request, reportbyproj, request.user,
                                     True):
        return render(request, 'global/permission_denied.html')

    # FIXME: Seria genial si se puede obtener la plantilla de reporte,
    # y si la plantilla de reporte tiene una fecha de cierre validarlo
    # también se le podría poner una opción que valide cual de los 2
    # comportamientos es deseado
    if reportbyproj.end_date and timezone.now() > reportbyproj.end_date:
        return redirect('informe_revisor', pk=reportbyproj.pk)
    if reportbyproj.start_date and timezone.now() < reportbyproj.start_date:
        return redirect(reverse('report_builder:report_out_of_datelimits',
                                kwargs={"pk": reportbyproj.pk}))
    if reportbyproj.state not in [RS_SUBMIT_PENDING, RS_EDITING]:
        return redirect('informe_revisor', pk=reportbyproj.pk)

    categories = process_template(
        request, reportbyproj.report, view_type='responsable',
        reportbyproj=reportbyproj)
    params = {'report': reportbyproj, 'categories': categories}
    return render(request, 'responsable/report.html', params)


@login_required
def report_out_of_datelimits(request, pk):
    '''
    Muestra un mensaje de que el informe se encuentra fuera de fecha, 
    esto es cuando se intenta ingresar a un informe por proyecto 
    que ya haya vencido o que todavía no se ha abierto.
    '''
    reportbyproj = get_object_or_404(ReportByProject, pk=pk)
    return render(request, 'report/out_of_datelimits.html',
                  {'report': reportbyproj})
