import random

from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext as _
from report_builder.models import Question, Answer
from ckeditor.widgets import CKEditorWidget
from report_builder.registry import models
from report_builder.catalogs import register_test_catalogs


class QuestionForm(forms.ModelForm):
    children = forms.CharField

    class Meta:
        model = Question
        fields = ('text', 'help', 'required', 'id')
        widgets = {
            'text': forms.Textarea(attrs={
                'rows': 6,
                'placeholder': 'Write your question here',
                'class': 'form-control'
            }),
            'help': forms.Textarea(attrs={
                'cols': 80,
                'rows': 5,
                'placeholder': 'A little help never hurts',
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
                'placeholder': 'Annotations',
                'class': 'form-control'
            }),
            'text': forms.Textarea(attrs={
                'id': 'foo',
                'rows': 6,
                'placeholder': 'Write here your answer',
                'class': 'form-control'
            })
        }

    def save(self, db_use):
        instance = super(AnswerForm, self).save(db_use)
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

    class Meta:
        model = Question
        widgets = {
            'text': forms.Textarea(attrs={
                'rows': 6,
                'placeholder': 'Write your question here',
                'class': 'form-control'
            }),
            'help': forms.Textarea(attrs={
                'cols': 80,
                'rows': 5,
                'placeholder': 'A little help never hurts',
                'class': 'form-control'
            }),

        }
        fields = ('text', 'help', 'required', 'minimum', 'maximum', 'steps', 'id')


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


class UniqueSelectionAdminForm(QuestionForm):
    register_test_catalogs()
    CATALOGS = ((index, model[1]) for index, model in enumerate(models))
    catalog = forms.ChoiceField(choices=CATALOGS)
    display_fields = forms.Field(required=False)

    class Meta:
        model = Question
        fields = ('text', 'help', 'required', 'id')
        widgets = {
            'text': forms.Textarea(attrs={
                'rows': 6,
                'placeholder': 'Write your question here',
                'class': 'form-control'
            }),
            'help': forms.Textarea(attrs={
                'cols': 80,
                'rows': 5,
                'placeholder': 'A little help never hurts',
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
            print(catalog)
            super(UniqueSelectionAnswerForm, self).__init__(*args, **kwargs)
            self.fields['text'].choices = catalog
        else:
            super(UniqueSelectionAnswerForm, self).__init__(*args, **kwargs)
