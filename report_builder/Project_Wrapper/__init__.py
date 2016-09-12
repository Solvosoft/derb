from django.contrib.contenttypes.models import ContentType


def get_project_type_class(type):
    project_type = ContentType.objects.get(app_label=type.app_name, model=type.name)
    return project_type.model_class()


def get_project_report_class(report):
    return get_project_type_class(report.type)


def get_project_class(reportbyproject):
    '''
        TODO: docstring
    '''
    return get_project_type_class(reportbyproject.report.type)


def get_project(reportbyproject):
    '''
        TODO: docstring
    '''
    klass = get_project_class(reportbyproject)
    return klass.objects.filter(pk=reportbyproject.project.object_id)


def print_project_contenttype(kwargs, klass=None):
    '''
        TODO: docstring
    '''
    try:
        object = kwargs['report'].project.content_object
        klass = kwargs['report'].project.content_object.__class__
    except:
        if klass is None:
            return get_project(kwargs['report'])
    return klass.objects.filter(pk=object.pk)


def get_filtered_project(kwargs, filters):
    '''
        TODO: docstring
    '''
    parameters = {}
    klass = None
    if '__CLASS__' in filters:
        klass = filters['__CLASS__']
    project = print_project_contenttype(kwargs, klass=klass)

    if len(project) == 0:
        return project

    base = project
    for key, value in filters.items():
        if '__PROJECT__' == key:
            parameters[value] = project
        elif '__CLASS__' == key:
            base = value
        else:
            parameters[key] = value
    return base.objects.filter(**parameters)


def is_responsable_of_project(reportbyproject, user, responsable=None):
    '''
        Checks if an user is the responsable of the given report by project
    '''
    project_class = get_project_class(reportbyproject)
    project_instance = project_class()
    project_list = project_instance.get_projects_by_responsable(user, responsable=responsable)
    return reportbyproject.project.object_id in project_list