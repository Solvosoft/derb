import datetime
import json

from async_notifications.models import EmailTemplate
from django.contrib.auth.models import User
from django.urls import reverse

from report_builder.Question.tests import QuestionViewAdminTest, QuestionViewRespTest
from report_builder.Question.tests import QuestionFormTest

from report_builder.models import Question, Answer, Report, ReportByProject, ReportType


class TableQuestionViewAdminTest(QuestionViewAdminTest):
    url = 'report_builder:table_question_admin'
    
    def setUp(self):
        data = {
                'catalog': '0',
                'displays': ['code','name'], 
                'headers': ['Code of your city?', 'Name of your city?']
        }
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
            class_to_load='table_question',
            text='NEW QUESTION TEXT',
            help='NEW QUESTION HELP',
            answer_options= json.dumps(data),
            required=Question.OPTIONAL
        )
    
    def test_post_create_with_correct_arguments_with_login(self):
        user = User.objects.first()
        report = Report.objects.first()
        url = reverse(self.url, kwargs={
            'report_pk': report.pk
        })
        data = {
            'text': 'NEW TABLE QUESTION',
            'help': 'NEW TABLE QUESTION HELP',
            'required': 0,
            'catalog': 0,
            'header_0': 'Code of your city?',
            'display_field_0': ['code'],
            'header_1': 'Name of your city?',
            'display_field_1': ['name'],
            'children': '{}'
        }

        self.client.login(username=user.username, password='test')
        resp = self.client.post(url, data=data)

        new_question = Question.objects.last()
        
        expected_answer_options = {
            'displays': ['code','name'],
            'headers': ['Code of your city?','Name of your city?'],
            'catalog': '0'
        }
        
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(new_question.text, 'NEW TABLE QUESTION')
        self.assertEqual(new_question.help, 'NEW TABLE QUESTION HELP')
        self.assertEqual(new_question.required, 0)
        self.assertEqual(json.loads(new_question.answer_options), expected_answer_options)

    def test_post_update_with_correct_arguments_with_login(self):
        user = User.objects.first()
        report = Report.objects.first()
        question = Question.objects.first()
        url = reverse(self.url, kwargs={
            'report_pk': report.pk,
            'question_pk': question.pk
        })
        data = {
            'text': 'NEW TABLE QUESTION',
            'help': 'NEW TABLE QUESTION HELP',
            'required': 0,
            'catalog': 0,
            'header_0': 'Code of your city?',
            'display_field_0': ['code'],
            'header_1': 'Name of your city?',
            'display_field_1': ['name'],
            'header_2': 'Where is located?',
            'display_field_2': ['location'],
            'children': '{}'
        }

        self.client.login(username=user.username, password='test')
        resp = self.client.post(url, data=data)

        new_question = Question.objects.last()
        
        expected_answer_options = {
            'displays': ['code','name','location'],
            'headers': ['Code of your city?','Name of your city?','Where is located?'],
            'catalog': '0'
        }

        self.assertEqual(resp.status_code, 200)
        self.assertEqual(new_question.text, 'NEW TABLE QUESTION')
        self.assertEqual(new_question.help, 'NEW TABLE QUESTION HELP')
        self.assertEqual(new_question.required, 0)
        self.assertEqual(json.loads(new_question.answer_options), expected_answer_options)

    def test_post_create_with_incorrect_arguments_with_login(self):
        '''
        It is incorrect, because "capital" is not a display_field for the catalog "0"
        '''
        user = User.objects.first()
        report = Report.objects.first()
        url = reverse(self.url, kwargs={
            'report_pk': report.pk
        })
        data = {
            'text': 'NEW TABLE QUESTION',
            'help': 'NEW TABLE QUESTION HELP',
            'required': 0,
            'catalog': 0,
            'header_0': 'Code of your city?',
            'display_field_0': ['code'],
            'header_1': 'Name of your country?',
            'display_field_1': ['capital'],
            'children': '{}'
        }

        self.client.login(username=user.username, password='test')
        resp = self.client.post(url, data=data)
        resp_str = str(resp.content)

        self.assertEqual(resp.status_code, 200)
        self.assertFalse(resp_str.isdigit())

    def test_post_update_with_incorrect_arguments_with_login(self):
        user = User.objects.first()
        report = Report.objects.first()
        question = Question.objects.first()
        url = reverse(self.url, kwargs={
            'report_pk': report.pk,
            'question_pk': question.pk
        })
        data = {
            'text': 'NEW TABLE QUESTION',
            'help': 'NEW TABLE QUESTION HELP',
            'required': 5,
            'catalog': 0,
            'header_0': 'Code of your city?',
            'display_field_0': ['code'],
            'header_1': 'Name of your city?',
            'display_field_1': ['name'],
            'children': '{}'
        }

        self.client.login(username=user.username, password='test')
        resp = self.client.post(url, data=data)
        resp_str = str(resp.content)

        self.assertEqual(resp.status_code, 200)
        self.assertFalse(resp_str.isdigit())

    def test_post_create_with_incomplete_arguments_with_login(self):
        user = User.objects.first()
        report = Report.objects.first()
        url = reverse(self.url, kwargs={
            'report_pk': report.pk
        })
        data = {
            'text': 'NEW TABLE QUESTION',
            'help': 'NEW TABLE QUESTION HELP',
            'catalog': 0,
            'header_0': 'Code of your city?',
            'display_field_0': ['code'],
            'children': '{}'
        }

        self.client.login(username=user.username, password='test')
        resp = self.client.post(url, data=data)
        resp_str = str(resp.content)

        self.assertEqual(resp.status_code, 200)
        self.assertFalse(resp_str.isdigit())

    def test_post_update_with_incomplete_arguments_with_login(self):
        user = User.objects.first()
        report = Report.objects.first()
        question = Question.objects.first()
        url = reverse(self.url, kwargs={
            'report_pk': report.pk,
            'question_pk': question.pk
        })
        data = {
            'text': 'NEW TABLE QUESTION',
            'help': 'NEW TABLE QUESTION HELP',
            'required': 0,
            'catalog': 0,
            'children': '{}'
        }

        self.client.login(username=user.username, password='test')
        resp = self.client.post(url, data=data)
        resp_str = str(resp.content)

        self.assertEqual(resp.status_code, 200)
        self.assertFalse(resp_str.isdigit())

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