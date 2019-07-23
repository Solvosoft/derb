from django import template
from django.contrib.contenttypes.models import ContentType
from django.utils.safestring import mark_safe

register = template.Library()


@register.filter
def get_project(reportbyproj):
    type = reportbyproj.report.type
    app_name = type.app_name
    name = type.name

    project_type = ContentType.objects.get(app_label=app_name, model=name)
    klass = project_type.model_class()
    setattr(reportbyproj, 'projects', klass.objects.get(
        pk=reportbyproj.project.object_id))
    return ''


@register.filter
def project_actions(text):
    return_value = 'No actions'
    if text:
        return_value = u'<div class="table-responsive"><table class="table table-bordered table-hover">' \
            '<tr class="success"><th class="text-center">Role</th> <th class="text-center">Name</th>' \
            '<th class="text-center">Date</th> <th class="text-center">Action</th> </tr>'
        for action in text.split('\n'):
            return_value += '<tr>'
            fields = action.split('\t')
            if len(fields) > 1:
                for field in fields:
                    return_value += '<td>%s</td>' % (field)
            return_value += '</tr>'
        return_value += '</table></div>'
    return mark_safe(return_value)
