import json
import random

from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext as _
from report_builder.models import Question, Answer, Observation
from ckeditor.widgets import CKEditorWidget
from report_builder.catalogs import register_test_catalogs
from report_builder.registry import models


class QuestionForm(forms.ModelForm):
    children = forms.CharField

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
        fields = ('text', 'help', 'id', 'required')
        widgets = {
            'text': CKEditorWidget(config_name='default'),
            'help': CKEditorWidget(config_name='default')
        }

    def save(self, db_use):
        instance = super(SimpleTextQuestionForm, self).save(db_use)
        instance.display_text = instance.text
        return instance


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
            }
        else:
            super(IntegerAnswerForm, self).__init__(*args, **kwargs)


# Float answer form
class FloatAnswerForm(IntegerAnswerForm):
    text = forms.DecimalField()


class UniqueSelectionQuestionForm(QuestionForm):
    register_test_catalogs()
    CATALOGS = ((index, model[1].capitalize()) for index, model in enumerate(models))
    catalog = forms.ChoiceField(choices=CATALOGS, widget=forms.Select(attrs={'class': 'form-control'}))
    display_fields = forms.Field(required=False)

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
    CATALOGS = ((index, model[1].capitalize()) for index, model in enumerate(models))
    catalog = forms.ChoiceField(choices=CATALOGS, widget=forms.Select(attrs={'class': 'form-control'}))
    header_0 = forms.CharField(max_length=100)
    display_field_0 = forms.ChoiceField()

    def __init__(self, *args, **kwargs):
        count = kwargs.pop('extra')
        super(TableQuestionForm, self).__init__(*args, **kwargs)

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
    display_fields_0 = forms.ChoiceField(widget=forms.Select(attrs={'class': 'form-control'}));
    
    def __init__(self, *args, **kwargs):
        catalog = kwargs.pop('extra')
        super(TableQuestionAnswerForm, self).__init__(*args, **kwargs)
        self.fields['display_fields_0'].choices = catalog