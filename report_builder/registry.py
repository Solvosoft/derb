import types
from django.utils.html import mark_safe
from report_builder.Project_Wrapper import get_filtered_project
from report_builder.encoding import _st
from report_builder.html_parser import KeyHandler

models = []
view_list = []


def get_fields(model, count=0, prefix='', exclude=None):
    return_fields = []
    if not exclude:
        exclude = []
    if count < 4:
        fields = []
        fields += model._meta.fields

        if hasattr(model._meta, 'many_to_many'):
            fields += model._meta.many_to_many

        for field in fields:
            if field.name != 'id' and not field.name in exclude and not prefix + str(field.name) in exclude:
                return_fields.append((prefix + str(field.name), field.verbose_name))
                if hasattr(field, 'related'):
                    exclude.append(field.name)
                    try:
                        parent_model = field.related.parent_model
                    except:
                        parent_model = field.related.model
                    return_fields += get_fields(parent_model, prefix=prefix + str(field.name) + '__', exclude=exclude,
                                                count=count + 1)
    return return_fields


def register(model, name=None, human_name=None, fields=None, exclude=None, type='select', func=None, related=None,
             extras=None, filters=None, derb_type='__ALL__'):
    '''
        TODO: docstring
    '''
    query = None
    if hasattr(model, '_meta'):
        query = model.objects.all()
    else:
        if not hasattr(model, 'model'):
            raise ValueError('Not a queryset nor model')
        query = model
        model = model.model

    if exclude is None:
        exclude = []

    if fields is None:
        if related is None:
            fields = get_fields(model, count=0, exclude=exclude)
        else:
            fields = get_fields(related, count=0, exclude=exclude)

    if extras is not None:
        fields += extras

    if name is None:
        name = model._meta.model_name

    if human_name is None:
        human_name = model._meta.verbose_name

    models.append((query, name, human_name, fields, type, func, filters, derb_type))


def get_properties_by_name(name, type='select'):
    '''
        TODO: docstring
    '''
    model = None
    for m in models:
        if m[1] == name and m[4] == type:
            model = m
            break
    return model


def get_value_field(model, field):
    '''
    TODO: docstring
    '''
    value = ''
    data = None

    if '__' in field and field != '__str__':
        sfield = field.split('__')
        if hasattr(model, sfield[0]):
            data = getattr(model, sfield[0])
            next_field = '__'.join(sfield[1:])
            if next_field == 'str__' and '__str__' in field:
                next_field = '__str__'
            value = get_value_field(data, next_field)
    else:
        if hasattr(model, field):
            data = getattr(model, field)
            if hasattr(model, 'get_' + field + '_display'):
                data = getattr(model, 'get_' + field + '_display')()
            if field == '__str__':
                field = field()
            if type(data) == types.MethodType:
                data = data()
            value = _st(data)

    return value


def get_queryset(name, type, context=None):
    '''
        Process de data recovery.
        See :func: `register` for usage examples
    '''
    model = get_properties_by_name(name, type)

    if model is not None:
        queryset = model[0]
        if context is not None:
            context['queryset'] = model[0]
            if model[6] is not None:    # filters
                queryset = get_filtered_project(context, model[6])
                context['filtered_query'] = queryset

            if model[5] is not None:    # function
                queryset = model[5](context)

    return model, queryset


def get_processed_fields(name, fields=None, watch=None, schema='', type='select', context=None):
    '''
        TODO: docstring
    '''
    sequence = []

    if not schema:
        if watch is not None:
            for attribute in watch:
                schema += '%(' + attribute + ')s '
            else:
                schema += '%(__str__)s'

    model, queryset = get_queryset(name, type, context=context)

    if model is not None:

        if watch is None:
            watch = ('__str__',)

        with_listings = False
        for q in queryset:
            show = {}
            if not with_listings:
                parser = KeyHandler()
                html = parser.feed(schema)
                with_listings = parser.is_dynamic()

            if fields is None or q.pk in fields:
                for value in watch:
                    show[value] = get_value_field(q, value)

                if len(show) == 0:
                    show['__str__'] = _st(q)

                parser.apply_keys(show)
                sequence.append((q.pk, mark_safe(str(parser))))

        if with_listings:
            sequence = [(1, mark_safe(str(parser)))]
    return sequence


def get_fields_tree(type='select', derb_type='__ALL__'):
    '''
        TODO: docstring
    '''
    registries = {}
    for registry in models:
        if registry[4] == type and (registry[7] == derb_type or registry[7] == '__ALL__'):
            registries[registry[1]] = {}
            for field in registry[3]:
                if '__' in field[0]:
                    sfield = field[0].split('__')
                    if not sfield[0] in registries[registry[1]]:
                        registries[registry[1]][sfield[0]] = []
                    registries[registry[1]][sfield[0]].append(field)
                else:
                    if not registry[1] in registries[registry[1]]:
                        registries[registry[1]][registry[1]] = []
                    registries[registry[1]][registry[1]].append(field)

    return registries


def get_field_types(options, catalog, type='select'):
    '''
        TODO: docstring
    '''
    types = {}
    properties = get_properties_by_name(catalog, type)
    if properties is not None:
        for option in options:
            attr = ""
            if '__' in option:
                attributes = option.split('__')
                name = attributes[0]
                attr = attributes[1]
            else:
                name = option

            model = properties[0].model
            field = model._meta.get_field_by_name(name)[0]
            if attr != '':
                field = field.related.parent_model._meta.get_field_by_name(attr)[0]
            klass = field.__class__.__name__
            display_name = field.verbose_name
            help = field.help_text
            types[option] = (klass, display_name, help)

    return types


def get_main_class(name, type='select'):
    '''
        TODO: docstring
    '''
    model = get_properties_by_name(name, type)
    if model:
        return model[0].model


def get_model_list(type, derb_type='__ALL__'):
    return_value = []

    for model in models:
        if model[4] == type and (model[7] == derb_type or model[7] == '__ALL__'):
            return_value.append((model[1], model[2]))

    return return_value


def register_initial_view(view, title, order, validator):
    view_list.append((view, title, order, validator))
    view_list.sort(cmp=lambda x,y: cmp(x[2], y[2]))