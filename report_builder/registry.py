from functools import cmp_to_key
import types

from django.utils.html import mark_safe

from report_builder.Project_Wrapper import get_filtered_project
from report_builder.encoding import _st
from report_builder.html_parser import KeyHandler

models = []
view_list = []


def get_fields(model, count=0, prefix='', exclude=None):
    '''
        Given a model, obtains its attributes and all its relation's attributes to a 4 degree depth.
        If the 'exclude' argument is provided, any attribute can be ignored. If 'exclude' refers to a relation
        attribute, the depth search for that attribute is stopped for that relation.

        The relations between models are represented with *__* (__), just like with Querysets in Django ORM.

        .. note:: by default ``id`` is not added to the attribute list returned
    :param models.Model model: class to apply the instrospection
    :param number count: relation depth level, if greater than 4, this parameter is ignored
    :param str prefix: prefix for the attribute lookup
    :param List exclude: attribute list to exclude
    :return: attribute list. For instance ['attr1', 'attr1__subattr2']
    '''
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
                return_fields.append(
                    (prefix + str(field.name), field.verbose_name))
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

    models.append(
        (query, name, human_name, fields, type, func, filters, derb_type))


def get_properties_by_name(name, type='select'):
    '''
        Looks into the registered models to match a given name

    :param str name: model name to lookup
    :param str type: catalog type
    :rtype tuple
    :return: a tuple like this: (query, name, human_name, fields [tuple], type, function, filters)
    '''
    model = None
    for m in models:
        if m[1] == name and m[4] == type:
            model = m
            break
    return model


def get_value_field(model, field):
    '''
        Given a model instance and Django queryset styled field name, (field1__attr2__attr3)
        returns the field's value, no matter how many depth levels reaches.

        If __str__ field is specified, the printing function is called for the previous attribute.
        For instance: field1__attr2__str__ returns the printing function for field1__attr2

        .. note:: Be careful, if no value matches the search, this function returns ''
    :param str model: model name for the lookup
    :param str field: field name for the lookup
    :return: field value for the lookup
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
            if model[6] is not None:  # filters
                queryset = get_filtered_project(context, model[6])
                context['filtered_query'] = queryset

            if model[5] is not None:  # function
                queryset = model[5](context)

    return model, queryset


def get_processed_fields(name, fields=None, watch=None, schema='', type='select', context=None):
    '''
    Given a modela name returns a list with query result.

    If *fields* is provided, the function returns only the objects with pks that match this list.

    .. note:: if *watch* is not provided, __str__ function is used to show the model info.

    :param str name: model registered name
    :param List fields: pk list required to be displayed
    :param List watch: field list required to be presented
    :param str schema: how the fields want to be presented, it can be a string like %(attribute)s
    :param str type: catalog type to lookup
    :param dict context: context of the view
    :return: the sequence of fields for the given model
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
    Builds a fields tree for every registered model

    .. code:: python

        {
           'model_name': {
              'attribute': [ attr__attr, ... ]
              'relation_model': [ attr, ... ]
            }
        }

    .. note::
        The model attributes that don't belog to a relationship are included in a
        attribute list with the same name as the relationship model
    :param str type: catalog type to lookup
    :param str derb_type: derb view type
    :return: the fields tree for every registered model
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
    Given an attribute list (attr, attr__attr2, attr__attr3__attr2, ...) returns a dict
    with the description for every attribute

    .. code:: python

        {
            'option': (class name, human name, field's help),
            ...
        }
    :param List options: attribute list to query its information
    :param str catalog: catalog name to lookup its attributes
    :param str type: catalog type to lookup
    :rtype dict
    :return: dictionary with the attributes descriptions from the given model
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
                field = field.related.parent_model._meta.get_field_by_name(
                    attr)[0]
            klass = field.__class__.__name__
            display_name = field.verbose_name
            help = field.help_text
            types[option] = (klass, display_name, help)

    return types


def get_main_class(name, type='select'):
    '''
    Returns the model class by a given name
    :param str name: model name to look for its class
    :param type: catalog type to lookup
    :return models.Model
    :return: model class
    '''
    model = get_properties_by_name(name, type)
    if model:
        return model[0].model


def get_model_list(type, derb_type='__ALL__'):
    '''
    Retuns a list with the catalog fields that match a given type

    .. code:: python

        [ (name, human_name),
         ....
        ]
    :param str type: catalog type to lookup
    :param str derb_type: derb view type
    :rtype List
    :return: list of catalog fields
    '''
    return_value = []

    for model in models:
        if model[4] == type and (model[7] == derb_type or model[7] == '__ALL__'):
            return_value.append((model[1], model[2]))

    return return_value


def register_initial_view(view, title, order, validator):
    '''
    Register a initial view in the application by appending them to view_list,
    according to its view class, view title, order of presentation and validator
    '''
    view_list.append((view, title, order, validator))
    view_list.sort(key=cmp_to_key(lambda x, y:
                                  (x[2] > y[2]) - (x[2] < y[2])
                                  ))
