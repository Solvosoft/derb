from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext as _

from report_builder.models import Question, Answer
from report_builder.report_shortcuts import get_question_permission
from django.db.models.fields import DecimalField
from lib2to3.fixer_util import Attr


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
    
    

#Integer question
class IntegerQuestionForm(QuestionForm):
    
    minimum=forms.DecimalField()
    maximum=forms.DecimalField()
    steps=forms.DecimalField()
    
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
        fields = ('text', 'help', 'required', 'minimum', 'maximum','steps','id')
    


        