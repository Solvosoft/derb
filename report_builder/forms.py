from django import forms

from report_builder.models import Report

class AdminReportForm(forms.ModelForm):
    '''
        Form for creating and updating a Report object
        This is implementation is meant to be used in the admin report view
    '''
    template = forms.CharField(widget=forms.HiddenInput, max_length=1024**3, initial=' ')
    order = forms.CharField(widget=forms.HiddenInput, max_length=10, initial='-1')

    class Meta:
        model = Report
        exclude = ('type', 'questions')
