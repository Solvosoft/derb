from django import template
from django.utils.safestring import mark_safe
from report_builder.Question.forms import NumericalSubquestionForm

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


@register.filter(name='verbose_header')
def verbose_header(value):
    desc, numb = value.split('_')
    verbose_desc = ''
    for x in NumericalSubquestionForm.DESC_CHOICES:
        if x[0] == desc:
            verbose_desc = x[1]
    new_value = verbose_desc + ' ' + numb
    return new_value