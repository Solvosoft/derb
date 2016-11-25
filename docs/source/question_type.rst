This section show the question type supported in DERB
===========================================================

.. graphviz::

   digraph Pregunta { 

        Question -> QuestionView;
        QuestionView -> ModelInfo;
        QuestionView -> UniqueSelectionQuestion;
        QuestionView -> MultipleSelectionQuestion;
        QuestionView -> IntegerQuestion;
        QuestionView -> SimpleTextQuestion;
        QuestionView -> BooleanQuestion;
        IntegerQuestion -> FloatQuestion;
        ModelInfo -> QuestionModelInfo;
        ModelInfo -> TableQuestion;

    } 


Question type list
___________________

.. toctree::
   :maxdepth: 2

   question_type/boolean_question
   question_type/simple_text_question
   question_type/integer_question
   question_type/float_question
   question_type/multiple_selection_question
   question_type/unique_selection_question
   question_type/model_info
   question_type/table_question
   question_type/question_model_info




Question
_____________________

.. automodule:: report_builder.Question.QuestionView
    :members: 
    :undoc-members:
    :member-order: bysource


