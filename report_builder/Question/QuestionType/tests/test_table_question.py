import datetime

from async_notifications.models import EmailTemplate
from django.contrib.auth.models import User
from django.urls import reverse

from report_builder.Question.tests import QuestionViewAdminTest, QuestionViewRespTest
from report_builder.Question.tests import QuestionFormTest

from report_builder.models import Question, Answer, Report, ReportByProject, ReportType


class TableQuestionViewAdminTest(QuestionViewAdminTest):
    '''
        Override and extend your tests here
    '''
    pass

class TableQuestionViewRespTest(QuestionViewRespTest):
    '''
        Override and extend your tests here
    '''
    pass

class TableQuestionFormTest(QuestionFormTest):
    '''
        Override and extend your tests here
    '''
    pass