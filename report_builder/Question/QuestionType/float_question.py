from report_builder.Question.QuestionType.integer_question import IntegerQuestionAdmin
from report_builder.Question.forms import FloatQuestionForm


class FloatQuestionAdmin(IntegerQuestionAdmin):
    form_class = FloatQuestionForm
    template_name = 'admin/float_question.html'
    name = 'float_question'
    minimal_representation = {
        'human_readable_name': 'Decimal number question',
        'help': 'Allows you to make numerical questions',
        'color': '#330065'
    }
