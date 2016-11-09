from report_builder.Question.question_loader import register_view
from report_builder.Question.QuestionType.boolean_question import BooleanQuestionViewAdmin
from report_builder.Question.QuestionType.integer_question import IntegerQuestionViewAdmin
from report_builder.Question.QuestionType.float_question import FloatQuestionViewAdmin
from report_builder.Question.QuestionType.simple_text_question import SimpleTextQuestionViewAdmin
from report_builder.Question.QuestionType.unique_selection_question import UniqueSelectionQuestionViewAdmin
from report_builder.Question.QuestionType.table_question import TableQuestionViewAdmin
from report_builder.Question.QuestionType.multiple_selection_question import MultipleSelectionQuestionViewAdmin
from report_builder.Question.QuestionType.model_info import ModelInfoViewAdmin

def register_admin_views():
    admin_views = [
        BooleanQuestionViewAdmin,
        IntegerQuestionViewAdmin,
        FloatQuestionViewAdmin,
        SimpleTextQuestionViewAdmin,
        UniqueSelectionQuestionViewAdmin,
        TableQuestionViewAdmin,
        MultipleSelectionQuestionViewAdmin,
        ModelInfoViewAdmin
    ]

    for view in admin_views:
        register_view(view, view_type='admin')