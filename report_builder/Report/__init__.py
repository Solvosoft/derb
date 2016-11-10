from datetime import date

from django.contrib.contenttypes.models import ContentType
from django.db.models import Q

from report_builder.Project_Wrapper import get_project
from report_builder.models import ReportType, Report, ReportByProject

RESPONSABLE = 0
ADVISOR = 1


def get_current_report(type=None, app_name=None, name=None):
    '''
        TODO: docstring
    '''
    if type is None:
        if app_name is None or name is None:
            raise Exception('No report type provided')
        type = ReportType.objects.get(app_name=app_name, name=name)
    return Report.objects.filter(type=type, opening_date__lte=date.today()).order_by('opening_date').last()


def get_manager(current):
    '''
        TODO: docstring
    '''
    manager = ReportByProject.objects
    if current:
        manager = ReportByProject.current
    return manager


def get_reports_by_user(user, _type=RESPONSABLE, report_type=None, current=False):
    '''
        TODO: docstring
    :return:
    '''
    return_value = {
        'responsable': [],
        'advisor': [],
        'collaborator': []
    }

    if report_type is None:
        report_type = ReportType.objects.all()

    if _type == ADVISOR:
        manager = ReportByProject.objects
    else:
        manager = get_manager(current)

    for rtype in report_type:
        try:
            project = ContentType.objects.get(
                app_label=rtype.app_name, model=rtype.name)
        except:
            continue

        project = project.model_class()()
        if type == RESPONSABLE:
            proj_responsable = project.get_project_by_responsable(
                user, responsable=True)
            proj_collaborator = project.get_project_by_responsable(
                user, responsable=False)

            return_value['responsable'] += list(
                manager.filter(report_type=rtype, project__object_id__in=proj_responsable))
            return_value['collaborator'] += list(
                manager.filter(report_type=rtype, project__object_id__in=proj_collaborator))
        else:
            projects_pks = project.get_project_by_advisor(user)
            result = manager.filter(
                report__type=rtype, project__object_id__in=projects_pks)
            ordered_result = result.order_by('-submit_date', 'project')
            result = []
            today = date.today()
            for res in ordered_result:
                if res.submit_date.year >= today.year - 2:
                    result.append(res)

            return_value['advisor'] += list(result)

    return return_value


def report_conflict(project_pk, report_type, start_date, submit_date, exclude=None):
    '''
        TODO: docstring
    '''
    conflict = False

    query = Q(start_date__gte=start_date, submit_date__lte=submit_date) | \
        Q(start_date__gte=start_date, start_date__lte=submit_date, submit_date__gte=submit_date) | \
        Q(Q(submit_date__gte=start_date), start_date__lte=start_date, submit_data__gte=submit_date) | \
        Q(start_date__lte=start_date, submit_date__gte=start_date,
          submit_date__lte=submit_date)

    reportbyproj = ReportByProject.objects.filter(
        query, project__object_id=project_pk, report__type=report_type)

    if exclude:
        reportbyproj = reportbyproj.exclude(pk=exclude)

    if len(reportbyproj):
        conflict = True

    return conflict


def get_responsable_emails_by_project(reportbyproj):
    '''
        TODO: docstring
    '''
    filtered_project = get_project(reportbyproj)
    responsables = []
    emails = ''

    if len(filtered_project) > 0:
        project = filtered_project[0]
        responsables = project.project_responsables()
        for responsable in responsables:
            emails += responsable.email + '; '

    return emails
