import datetime
import json

from async_notifications.models import EmailTemplate
from django.contrib.auth.models import User
from django.urls import reverse

from report_builder.Question.tests import QuestionViewAdminTest, QuestionViewRespTest
from report_builder.Question.tests import QuestionFormTest

from report_builder.models import Question, Answer, Report, ReportByProject, ReportType, Project


class UniqueSelectionQuestionViewAdminTest(QuestionViewAdminTest):
    url = 'report_builder:unique_selection_admin'
    
    def setUp(self):
        User.objects.create_user(username='test', password='test')
        report_type = ReportType.objects.create(
            type='test_type',
            name='test_name',
            app_name='test.app',
            action_ok=EmailTemplate.objects.create(code='ok_report_type_test', subject='', message=''),
            revision_turn=EmailTemplate.objects.create(code='turn_report_type_test', subject='', message=''),
            responsable_change=EmailTemplate.objects.create(code='change_report_type_test', subject='', message=''),
            report_start=EmailTemplate.objects.create(code='start_report_type_test', subject='', message=''),
            report_end=EmailTemplate.objects.create(code='end_report_type_test', subject='', message='')
        )
        report = Report.objects.create(type=report_type, name='Test report', opening_date=datetime.date.today())
        Question.objects.create(
            report=report,
            class_to_load='unique_selection_question',
            text='NEW UNIQUE QUESTION',
            help='NEW UNIQUE QUESTION HELP',
            answer_options='{\"display_fields\": [\"name\"], \"catalog\": [\"0\"], \"widget\": [\"radiobox\"]}',
            required=Question.OPTIONAL
        )
    
    def test_post_create_with_correct_arguments_with_login(self):
        user = User.objects.first()
        report = Report.objects.first()
        url = reverse(self.url, kwargs={
            'report_pk': report.pk
        })
        data = {
            'text': 'NEW UNIQUE QUESTION',
            'help': 'NEW UNIQUE QUESTION HELP',
            'required': 0,
            'catalog': 0,
            'widget': 'radiobox',
            'display_fields': ['name'],
            'children': '{}',
            'schema': ''
        }

        self.client.login(username=user.username, password='test')
        resp = self.client.post(url, data=data)

        new_question = Question.objects.last()

        expected_answer_options = {
            'children': {},
            'display_fields': ['name'],
            'schema': '',
            'widget': 'radiobox',
            'catalog': '0'
        }

        self.assertEqual(resp.status_code, 200)
        self.assertEqual(new_question.text, 'NEW UNIQUE QUESTION')
        self.assertEqual(new_question.help, 'NEW UNIQUE QUESTION HELP')
        self.assertEqual(new_question.required, 0)
        self.assertEqual(json.loads(new_question.answer_options), expected_answer_options)

   
class UniqueSelectionQuestionViewRespTest(QuestionViewRespTest):
    '''
        Override and extend your tests here
    '''
    pass

class UniqueSelectionQuestionFormTest(QuestionFormTest):
    '''
        Override and extend your tests here
    '''
    pass