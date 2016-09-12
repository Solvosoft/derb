from django import template
from django.utils.safestring import mark_safe

register = template.Library()


@register.filter
def is_jquery_widget(field, prefix=''):
    return_value = ''

    datepicker = '<script>$(document).ready(function(){$("%s").datepicker({dateFormat: \'dd/mm/yy\'})});</script>'
    cke_editor = '<script>$(document).ready(function(){poner_cke_onchange("%s");});</script>'
    type = field.field.__class__.__name__

    if prefix:
        prefix = '.' + str(prefix)

    if type == 'DateField':
        return_value = datepicker % (prefix + ' #' + str(field.id_for_label))

    if type == 'BleachField':
        return_value = cke_editor % (str(field.id_for_label))

    return mark_safe(return_value)