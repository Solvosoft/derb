import json

from report_builder.Question.QuestionType.unique_selection_question import UniqueSelectionQuestionViewAdmin
from report_builder.Question.forms import ModelInfoQuestionForm
from report_builder.models import Question as QuestionModel


class ModelInfoViewAdmin(UniqueSelectionQuestionViewAdmin):
    template_name = 'admin/question_types/model_info.html'
    name = 'model_info'
    form_class = ModelInfoQuestionForm
    answer_options = None
    minimal_representation = {
        'human_readable_name': 'Model information',
        'help': 'Allows you to insert HTML info into the report',
        'color': '#72e1d1'
    }
    registry_type = 'information'

    def additional_template_parameters(self, **kwargs):
        parameters = super(ModelInfoViewAdmin, self).additional_template_parameters(**kwargs)
        parameters.update({
            'is_info': True
        })
        return parameters

    def pre_save(self, object, request, form):
        object = super(ModelInfoViewAdmin, self).pre_save(object, request, form)
        object.required = QuestionModel.OPTIONAL
        answer_options = {}
        if object.answer_options:
            answer_options = json.loads(object.answer_options)

        on_modal = form.cleaned_data['on_modal']
        answer_options['on_modal'] = on_modal
        object.answer_options = json.dumps(answer_options)
        object.text = form.cleaned_data['text']
        return object

    def get_form(self, post=None, instance=None, extra=None):
        if extra is None: extra = {}
        answer_options = self.get_question_answer_options()
        on_modal = False
        if answer_options is not None and 'on_modal' in answer_options:
            on_modal = answer_options['on_modal']

        extra.update({
            'form_number': str(self.form_number),
            'on_modal': on_modal
        })
        print(extra)

        return super(ModelInfoViewAdmin, self).get_form(post=post, instance=instance, extra=extra)
