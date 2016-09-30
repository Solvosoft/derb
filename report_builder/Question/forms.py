from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext as _

from report_builder.models import Question, Answer
from report_builder.report_shortcuts import get_question_permission

from report_builder.registry import models, get_value_field
from report_builder.catalogs import register_test_catalogs

import json

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

#Unique_Selection_Question
class UniqueSelectionAdminForm(QuestionForm):
    register_test_catalogs()
    CATALOGS = ((index, model[1]) for index, model in enumerate(models))
    catalog = forms.ChoiceField(choices=CATALOGS)
    display_fields = forms.MultipleChoiceField(choices=models[0][3], widget=forms.CheckboxSelectMultiple, required=False)
    
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
        
class UniqueSelectionAnswerForm(AnswerForm):
    fields = forms.ChoiceField(widget=forms.Select, choices=objects)

        
    
    