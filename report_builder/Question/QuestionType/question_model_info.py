from report_builder.Question.QuestionType.model_info import ModelInfoViewAdmin
from report_builder.Question.forms import QuestionModelInfoQuestionForm


class QuestionModelInfoViewAdmin(ModelInfoViewAdmin):
    template_name = 'admin/question_types/question_model_info.html'
    name = 'question_model_info'
    form_class = QuestionModelInfoQuestionForm
    answer_options = None
    minimal_representation = {
        'human_readable_name': 'Model information with related questions',
        'help': 'Allows you to created related questions for every option of a given catalog',
        'color': '#c0dfa1'
    }
    registry_type = 'question_information'

    def additional_template_parameters(self, **kwargs):
        parameters = super(QuestionModelInfoViewAdmin, self).additional_template_parameters(**kwargs)
        if not parameters: parameters = {}
        parameters['questions'] = self.process_children(self.request, parameters, kwargs)
        parameters['is_info'] = True
        return parameters
