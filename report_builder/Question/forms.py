import random

from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext as _

from report_builder.models import Question, Answer
from report_builder.report_shortcuts import get_question_permission

from ckeditor.widgets import CKEditorWidget
from watchdog.utils.decorators import attrs

from bs4 import BeautifulSoup


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
    
class SimpleTextAnswerForm(forms.ModelForm):
    
    class Meta:
        model = Question
        fields = ('text', 'help', 'id','required')
        widgets = {
            'text': CKEditorWidget(config_name='default'),
            'help': CKEditorWidget(config_name='default')
        }
        

#Simple_Text_Question
class SimpleTextQuestionForm(SimpleTextAnswerForm):
    
    
    def save(self, db_use):
        instance = super(SimpleTextQuestionForm, self).save(db_use)
        instance.display_text = instance.text
        return instance