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
    
    

#Integer question
class IntegerQuestionForm(QuestionForm):
    
    
    MINIMUM =((p,p) for p in range(0,99))
    minimum = forms.ChoiceField(choices=MINIMUM)
    MAXIMUM =((p,p) for p in range(99,200))
    maximum = forms.ChoiceField(choices=MAXIMUM)
    STEPS =((p,p) for p in range(100,200))
    steps = forms.ChoiceField(choices=STEPS)
    
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
            })
            
                   
        }
        fields = ('text', 'help', 'required', 'minimum', 'maximum','steps','id')
    


        