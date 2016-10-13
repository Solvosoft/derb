from report_builder.Question.QuestionType.integer_question import IntegerQuestionAdmin
from report_builder.Question.QuestionType.integer_question import IntegerQuestionResp
from report_builder.Question.QuestionType.integer_question import IntegerQuestionViewPDF
from report_builder.Question.forms import FloatAnswerForm


class FloatQuestionAdmin(IntegerQuestionAdmin):
    template_name = 'admin/float_question.html'
    name = 'float_question'
    minimal_representation = {
        'human_readable_name': 'Decimal number question',
        'help': 'Allows you to make numerical questions',
        'color': '#330065'
    }

class FloatQuestionResp(IntegerQuestionResp):
    template_name = 'responsable/float_question.html'
    name = 'float_question'
    form_class = FloatAnswerForm

class FloatQuestionPDF(IntegerQuestionViewPDF):
    name = 'float_question'
    template_name = 'pdf/float_question.html'