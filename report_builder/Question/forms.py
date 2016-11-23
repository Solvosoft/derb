import json
import random

from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext as _

from report_builder.models import Question, Answer, Observation
from ckeditor.widgets import CKEditorWidget
from report_builder.registry import models
from ast import literal_eval

class QuestionForm(forms.ModelForm):
    children = forms.CharField(widget=forms.HiddenInput, required=False)

    class Meta:
        model = Question
        fields = ('text', 'help', 'required', 'id')
        widgets = {
            'text': forms.Textarea(attrs={
                'rows': 6,
                'placeholder': _('Write your question here'),
                'class': 'form-control'
            }),
            'help': forms.Textarea(attrs={
                'cols': 80,
                'rows': 5,
                'placeholder': _('A little help never hurts'),
                'class': 'form-control'
            })
        }
        exclude = ('order',)


class AnswerForm(forms.ModelForm):
    """
        TODO: docstring
    """

    def clean_text(self):
        text = self.cleaned_data['text']
        # required = get_question_permission(self.instance.question)
        if not text:
            raise ValidationError(_('This field is required'), code='required')
        return text

    class Meta:
        model = Answer
        fields = ('annotation', 'text')
        widgets = {
            'annotation': forms.Textarea(attrs={
                'id': 'foo',
                'rows': 9,
                'placeholder': _('Annotations'),
                'class': 'form-control'
            }),
            'text': forms.Textarea(attrs={
                'id': 'foo',
                'rows': 6,
                'placeholder': _('Write here your answer'),
                'class': 'form-control'
            })
        }

    def save(self, db_use):
        instance = super(AnswerForm, self).save(db_use)
        instance.display_text = instance.text
        return instance
    

class ObservationForm(forms.ModelForm):
    class Meta:
        model = Observation
        fields = ('text',)
        widgets = {
            'text': forms.Textarea(attrs={
                'rows': 6,
                'placeholder': _('Write here your observation'),
                'class': 'form-control'
            })
        }
        

class SimpleTextAnswerForm(AnswerForm):
    class Meta:
        model = Answer
        fields = ('text', 'annotation')
        widgets = {
            'text': CKEditorWidget(config_name='default'),
            'annotation': CKEditorWidget(config_name='default')
        }

    def save(self, db_use):
        instance = super(SimpleTextAnswerForm, self).save(db_use)
        instance.display_text = instance.text
        return instance


# Simple_Text_Question
class SimpleTextQuestionForm(QuestionForm):
    class Meta:
        model = Question
        fields = ('text', 'help', 'id')
        widgets = {
            'text': CKEditorWidget(config_name='default'),
            'help': CKEditorWidget(config_name='default')
        }

    def save(self, db_use):
        instance = super(SimpleTextQuestionForm, self).save(db_use)
        instance.display_text = instance.text
        return instance

    def __init__(self, *args, **kwargs):
        on_modal = False
        if 'extra' in kwargs:
            extra = kwargs.pop('extra')
            on_modal = extra['on_modal']
        super(SimpleTextQuestionForm, self).__init__(*args, **kwargs)

        self.fields['on_modal'] = forms.BooleanField(
            label='See on modal',
            required=False,
            initial=on_modal,
            widget=forms.CheckboxInput(
                attrs={
                    'onchange': 'request_name_button_info(this);'
                }
            )
        )


# Boolean answer form
class BooleanAnswerForm(AnswerForm):
    option = forms.ChoiceField
    attrs = {
        'onchange': 'show_related_question_boolean(this);'
    }
    choices = (('yes', 'Yes'), ('no', 'No'), ('na', 'Don\'t know/Don\'t answer'))

    def __init__(self, *args, **kwargs):
        self.attrs['id'] = 'combo_' + str(random.randint(5000, 10000))
        super(BooleanAnswerForm, self).__init__(*args, **kwargs)

        self.fields['text'] = self.option(widget=forms.RadioSelect(self.attrs), choices=self.choices)

    def save(self, db_use):
        instance = super(BooleanAnswerForm, self).save(db_use)
        selected_option = dict(self.fields['text'].choices)
        instance.display_text = selected_option[instance.text]
        return instance


# Integer question form
class IntegerQuestionForm(QuestionForm):
    minimum = forms.DecimalField(initial=0)
    maximum = forms.DecimalField(initial=100)
    steps = forms.DecimalField(initial=1)

    def __init__(self, *args, **kwargs):
        super(IntegerQuestionForm, self).__init__(*args, **kwargs)
        if 'instance' in kwargs:
            instance = kwargs.get('instance')
            if instance is not None:
                answer_options = json.loads(instance.answer_options)
                self.fields['minimum'].initial = answer_options['minimum']
                self.fields['maximum'].initial = answer_options['maximum']
                self.fields['steps'].initial = answer_options['steps']

    class Meta:
        model = Question
        widgets = {
            'text': forms.Textarea(attrs={
                'rows': 6,
                'placeholder': _('Write your question here'),
                'class': 'form-control'
            }),
            'help': forms.Textarea(attrs={
                'cols': 80,
                'rows': 5,
                'placeholder': _('A little help never hurts'),
                'class': 'form-control'
            }),

        }
        fields = ('text', 'help', 'required', 'minimum', 'maximum', 'steps')


# Integer answer form
class IntegerAnswerForm(AnswerForm):
    text = forms.IntegerField()

    def __init__(self, *args, **kwargs):
        if 'extra' in kwargs:
            answer_options = kwargs.pop('extra')
            super(IntegerAnswerForm, self).__init__(*args, **kwargs)
            self.fields['text'].initial = answer_options['minimum']
            self.fields['text'].min_value = answer_options['minimum']
            self.fields['text'].max_value = answer_options['maximum']
            self.fields['text'].widget.attrs = {
                'step': answer_options['steps'],
                'min': answer_options['minimum'],
                'max': answer_options['maximum'],

            }
        else:
            super(IntegerAnswerForm, self).__init__(*args, **kwargs)


# Float answer form
class FloatAnswerForm(IntegerAnswerForm):
    text = forms.DecimalField()


class UniqueSelectionQuestionForm(QuestionForm):
    catalog = forms.ChoiceField()
    display_fields = forms.Field(required=False)

    extra = None

    class Meta:
        model = Question
        fields = ('text', 'help', 'required', 'id')
        widgets = {
            'text': forms.Textarea(attrs={
                'rows': 6,
                'placeholder': _('Write your question here'),
                'class': 'form-control'
            }),
            'help': forms.Textarea(attrs={
                'cols': 80,
                'rows': 5,
                'placeholder': _('A little help never hurts'),
                'class': 'form-control'
            }),
            'required': forms.Select(attrs={
                'class': 'form-control'
            })
        }

    def __init__(self, *args, **kwargs):
        if 'extra' in kwargs:
            self.extra = kwargs.pop('extra')
        super(UniqueSelectionQuestionForm, self).__init__(*args, **kwargs)

        if self.extra is not None and 'widgets' in self.extra:
            widgets_choices = self.extra['widgets']
        else:
            widgets_choices = ()

        # Catalog
        catalog_choices = ((index, model[1].capitalize()) for index, model in enumerate(models))
        self.fields['catalog'].choices = catalog_choices
        initial_widget = None
        if self.extra and 'answer_options' in self.extra and self.extra['answer_options'] is not None:
            initial_widget = self.extra['answer_options']['widget'][0]

        # Widget
        if widgets_choices is not None:
            self.fields['widget'] = forms.ChoiceField(
                widget=forms.RadioSelect(attrs={
                    'id': str(random.randint(50, 10000)) + '_select'
                }),
                required=True,
                choices=widgets_choices,
                initial=initial_widget
            )


class UniqueSelectionAnswerForm(AnswerForm):
    text = forms.ChoiceField(widget=forms.Select(attrs={'class': 'form-control'}))

    def __init__(self, *args, **kwargs):
        if 'extra' in kwargs:
            catalog = kwargs.pop('extra')
            super(UniqueSelectionAnswerForm, self).__init__(*args, **kwargs)
            self.fields['text'].choices = catalog
        else:
            super(UniqueSelectionAnswerForm, self).__init__(*args, **kwargs)

    def save(self, db_use):
        instance = super(AnswerForm, self).save(db_use)
        object_pk = instance.text
        answer_options_json = instance.question.answer_options
        answer_options = json.loads(answer_options_json)
        catalog = int(answer_options['catalog'][0])
        display_fields = answer_options['display_fields']

        queryset = models[catalog][0]
        object = queryset.get(pk=object_pk)
        display_text = ''

        if display_fields is not None:
            for i, field in enumerate(display_fields):
                display_text += getattr(object, field)
                if (i + 1) != len(display_fields):
                    display_text += ' - '
        else:
            display_text = str(object)

        instance.display_text = display_text
        return instance


# Table_Question
class TableQuestionForm(QuestionForm):
    catalog = forms.ChoiceField()
    header_0 = forms.CharField(max_length=100)
    display_field_0 = forms.ChoiceField()

    def __init__(self, *args, **kwargs):
        count = kwargs.pop('extra')
        super(TableQuestionForm, self).__init__(*args, **kwargs)

        # Catalog
        catalog_choices = ((index, model[1].capitalize()) for index, model in enumerate(models))
        self.fields['catalog'].choices = catalog_choices

        for i in range(0, count):
            self.fields['header_%d' % i] = forms.CharField(max_length=100)
            self.fields['display_field_%d' % i] = forms.ChoiceField()

        if self.is_bound:
            catalog = self.data['catalog']
            for i in range(0, count):
                self.fields['display_field_%d' % i].choices = models[int(catalog)][3]

    class Meta:
        model = Question
        fields = ('text', 'help', 'required', 'id')
        widgets = {
            'text': forms.Textarea(attrs={
                'rows': 6,
                'placeholder': _('Write your question here'),
                'class': 'form-control'
            }),
            'help': forms.Textarea(attrs={
                'cols': 80,
                'rows': 5,
                'placeholder': _('A little help never hurts'),
                'class': 'form-control'
            }),
            'required': forms.Select(attrs={
                'class': 'form-control'
            })
        }


class TableQuestionAnswerForm(AnswerForm):
    def __init__(self, *args, **kwargs):
        extra = kwargs.pop('extra')
        catalog = extra['catalog_choices']
        headers = extra['headers']

        super(TableQuestionAnswerForm, self).__init__(*args, **kwargs)
        del self.fields['text']
        del self.fields['annotation']

        for i in range(0, len(catalog)):
            self.fields['display_field_%d' % i] = forms.ChoiceField(label=headers[i], widget=forms.Select(
                attrs={'class': 'form-control'}))

        for i in range(0, len(catalog)):
            self.fields['display_field_%d' % i].choices = catalog[i]

    def save(self, db_use):
        instance = super(AnswerForm, self).save(db_use)
        instance.text = str(sorted(self.cleaned_data.items()))

        display_text = ''
        for key, value in sorted(self.cleaned_data.items()):
            dictionary = dict(self.fields[key].choices)
            display_text += '%s: %s\n' % (self.fields[key].label, list(dictionary.values())[int(value)])
        instance.display_text = display_text
        return instance


# Multiple Selection Question
class MultipleSelectionQuestionForm(QuestionForm):
    catalog = forms.ChoiceField()
    display_fields = forms.Field(required=False)

    CHECKBOX = 0
    MULTIPLE_SELECT = 1
    COMBOBOX = 2
    WIDGET_CHOICES = (
        (CHECKBOX, _('Checkbox')),
        (MULTIPLE_SELECT, _('Multiple Select')),
        (COMBOBOX, _('Combobox'))
    )
    widget = forms.ChoiceField(
        widget=forms.RadioSelect(attrs={
            'id': str(random.randint(50, 10000)) + '_select'
        }),
        required=True,
        choices=WIDGET_CHOICES
    )

    def __init__(self, *args, **kwargs):
        super(MultipleSelectionQuestionForm, self).__init__(*args, **kwargs)

        # Catalog
        catalog_choices = ((index, model[1].capitalize()) for index, model in enumerate(models))
        self.fields['catalog'].choices = catalog_choices

        if 'instance' in kwargs:
            instance = kwargs.get('instance')
            if instance is not None:
                answer_options = json.loads(instance.answer_options)
                if 'widget' in answer_options:
                    self.fields['widget'].initial = answer_options['widget']

    class Meta:
        model = Question
        fields = ('text', 'help', 'required', 'id', 'widget')
        widgets = {
            'text': forms.Textarea(attrs={
                'rows': 6,
                'placeholder': _('Write your question here'),
                'class': 'form-control'
            }),
            'help': forms.Textarea(attrs={
                'cols': 80,
                'rows': 5,
                'placeholder': _('A little help never hurts'),
                'class': 'form-control'
            }),
            'required': forms.Select(attrs={
                'class': 'form-control'
            })
        }


class MultipleSelectionAnswerForm(AnswerForm):
    text = forms.ChoiceField()

    def __init__(self, *args, **kwargs):
        if 'extra' in kwargs:
            extra = kwargs.pop('extra')
            super(MultipleSelectionAnswerForm, self).__init__(*args, **kwargs)

            catalog = extra['catalog']
            widget = int(extra['widget'])

            if widget == MultipleSelectionQuestionForm.CHECKBOX:
                self.fields['text'] = forms.MultipleChoiceField(choices=catalog, widget=forms.CheckboxSelectMultiple)
            elif widget == MultipleSelectionQuestionForm.MULTIPLE_SELECT:
                self.fields['text'] = forms.MultipleChoiceField(choices=catalog)
            elif widget == MultipleSelectionQuestionForm.COMBOBOX:
                self.fields['text'] = forms.ChoiceField(choices=catalog)

        else:
            super(MultipleSelectionAnswerForm, self).__init__(*args, **kwargs)

    def save(self, db_use):
        instance = super(AnswerForm, self).save(db_use)
        objectpk = instance.text
        answer_options_json = instance.question.answer_options
        answer_options = json.loads(answer_options_json)
        catalog = int(answer_options['catalog'][0])
        display_fields = answer_options['display_fields']
        queryset = models[catalog][0]

        try:
            int(objectpk)
            print('es numero')
            object = queryset.get(pk=objectpk)
            display_text = ''
            for i, fild in enumerate(display_fields):
                display_text += getattr(object, fild)
                if (i + 1) != len(display_fields):
                    display_text += ' - '
            instance.display_text = display_text
            return instance

        except:
            object_pks = literal_eval(instance.text)
            queryset = queryset.filter(pk__in=object_pks)
            display_text = ''
            for o, object in enumerate(queryset):
                for i, field in enumerate(display_fields):
                    display_text += getattr(object, field)
                    if (i + 1) != len(display_fields):
                        display_text += ' - '
                if (o + 1) < len(queryset):
                    display_text += '\n'

            instance.display_text = display_text
            return instance


class ModelInfoQuestionForm(UniqueSelectionQuestionForm):
    with_text = 'text'

    class Meta:
        model = Question
        fields = ('text', 'help', 'id')

    def __init__(self, *args, **kwargs):
        self.post = args
        on_modal = False
        if 'extra' in kwargs:
            extra = kwargs.pop('extra')
            on_modal = extra['on_modal']

        super(ModelInfoQuestionForm, self).__init__(*args, **kwargs)

        del self.fields['widget']

        self.fields['on_modal'] = forms.BooleanField(
            label='See on modal',
            required=False,
            initial=on_modal,
            widget=forms.CheckboxInput(
                attrs={
                    'onchange': 'get_button_name_info(this);'
                }
            )
        )


class QuestionModelInfoQuestionForm(ModelInfoQuestionForm):
    with_text = 'text'

    class Meta:
        model = Question
        fields = ('text', 'help', 'id', 'required')

    def __init__(self, *args, **kwargs):
        self.post = args
        if 'extra' in kwargs:
            extra = kwargs.pop('extra')
        super(QuestionModelInfoQuestionForm, self).__init__(*args, **kwargs)
