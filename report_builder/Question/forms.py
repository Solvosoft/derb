import random

from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext as _

from report_builder.models import Question, Answer
from report_builder.report_shortcuts import get_question_permission


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
        required = get_question_permission(self.instance.question)
        if required == 1 and not text:
            raise ValidationError(_('This field is required'), code='required')
        return text

    class Meta:
        model = Answer
        fields = ('annotation', 'text')
        widgets = {
            'annotation': forms.Textarea(attrs={
                'rows': 9,
                'placeholder': 'Annotations',
                'class': 'form-control'
            }),
            'text': forms.Textarea(attrs={
                'rows': 6,
                'placeholder': 'Write here your answer',
                'class': 'form-control'
            })
        }

    def save(self, db_use):
        instance = super(AnswerForm, self).save(db_use)
        instance.display_text = instance.text
        return instance


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