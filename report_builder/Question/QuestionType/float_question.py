from report_builder.Question.QuestionType.integer_question import IntegerQuestionViewAdmin
from report_builder.Question.QuestionType.integer_question import IntegerQuestionViewResp
from report_builder.Question.QuestionType.integer_question import IntegerQuestionViewPDF
from report_builder.Question.forms import FloatAnswerForm


class FloatQuestionViewAdmin(IntegerQuestionViewAdmin):
    template_name = 'admin/float_question.html'
    name = 'float_question'
    minimal_representation = {
        'human_readable_name': 'Decimal number question',
        'help': 'Allows you to make numerical questions',
        'color': '#2e5eaa'
    }
    evaluator = float

class FloatQuestionViewResp(IntegerQuestionViewResp):
    template_name = 'responsable/float_question.html'
    name = 'float_question'
    form_class = FloatAnswerForm

class FloatQuestionViewPDF(IntegerQuestionViewPDF):
    name = 'float_question'
    template_name = 'pdf/float_question.html'