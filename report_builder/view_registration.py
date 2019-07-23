from report_builder.Question.QuestionType.boolean_question import (
    BooleanQuestionViewAdmin, BooleanQuestionViewResp)
from report_builder.Question.QuestionType.float_question import (
    FloatQuestionViewAdmin, FloatQuestionViewResp)
from report_builder.Question.QuestionType.integer_question import(
    IntegerQuestionViewAdmin, IntegerQuestionViewResp)
from report_builder.Question.QuestionType.model_info import (
    ModelInfoViewAdmin, ModelInfoViewResp)
from report_builder.Question.QuestionType.multiple_selection_question import(
    MultipleSelectionQuestionViewAdmin)
from report_builder.Question.QuestionType.question_model_info import (
    QuestionModelInfoViewAdmin)
from report_builder.Question.QuestionType.simple_text_question import (
    SimpleTextQuestionViewAdmin)
from report_builder.Question.QuestionType.table_question import (
    TableQuestionViewAdmin)
from report_builder.Question.QuestionType.unique_selection_question import (
    UniqueSelectionQuestionViewAdmin)
from report_builder.Question.question_loader import register_view


def register_admin_views():
    admin_views = [
        BooleanQuestionViewAdmin,
        IntegerQuestionViewAdmin,
        FloatQuestionViewAdmin,
        SimpleTextQuestionViewAdmin,
        UniqueSelectionQuestionViewAdmin,
        TableQuestionViewAdmin,
        MultipleSelectionQuestionViewAdmin,
        ModelInfoViewAdmin,
        QuestionModelInfoViewAdmin
    ]

    for view in admin_views:
        register_view(view, view_type='admin')


def register_responsable_views():
    for view in [BooleanQuestionViewResp,
                 IntegerQuestionViewResp,
                 FloatQuestionViewResp,
                 SimpleTextQuestionViewResp,
                 UniqueSelectionQuestionViewResp,
                 TableQuestionViewResp,
                 MultipleSelectionQuestionViewResp,
                 ModelInfoViewResp,
                 QuestionModelInfoViewResp]:
        register_view(view, view_type='responsable')
