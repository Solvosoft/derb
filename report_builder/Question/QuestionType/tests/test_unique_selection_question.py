import datetime
import json

from async_notifications.models import EmailTemplate
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.urls import reverse

from report_builder.Question.tests import QuestionViewAdminTest, QuestionViewRespTest
from report_builder.Question.tests import QuestionFormTest

from report_builder.models import Question, Answer, Report, ReportByProject, ReportType, Project, City, Country


class UniqueSelectionQuestionViewAdminTest(QuestionViewAdminTest):
    url = 'report_builder:unique_selection_admin'
    
    def setUp(self):
        data = {
                'display_fields': ['name'],
                'catalog': '0', 
                'widget': 'radiobox',
                'children': '{}', 
                'schema': ''
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
            class_to_load='unique_selection_question',
            text='NEW QUESTION TEXT',
            help='NEW QUESTION HELP',
            answer_options = json.dumps(data),
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

    def test_post_update_with_correct_arguments_with_login(self):
        user = User.objects.first()
        report = Report.objects.first()
        question = Question.objects.first()
        url = reverse(self.url, kwargs={
            'report_pk': report.pk,
            'question_pk': question.pk
        })
        data = {
            'text': 'NEW UNIQUE QUESTION',
            'help': 'NEW UNIQUE QUESTION HELP',
            'required': 2,
            'catalog': 0,
            'widget': 'radiobox',
            'display_fields': ['name','location'],
            'children': '{}',
            'schema': ''
        }

        self.client.login(username=user.username, password='test')
        resp = self.client.post(url, data=data)

        new_question = Question.objects.last()
        
        expected_answer_options = {
            'children': {},
            'display_fields': ['name','location'],
            'schema': '',
            'widget': 'radiobox',
            'catalog': '0'
        }

        self.assertEqual(resp.status_code, 200)
        self.assertEqual(new_question.text, 'NEW UNIQUE QUESTION')
        self.assertEqual(new_question.help, 'NEW UNIQUE QUESTION HELP')
        self.assertEqual(new_question.required, 2)
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
            'text': 'NEW UNIQUE QUESTION',
            'help': 'NEW UNIQUE QUESTION HELP',
            'required': 0,
            'catalog': 0,
            'widget': 'radiobox',
            'display_fields': ['capital'],
            'children': '{}',
            'schema': ''
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
            'text': 'NEW UNIQUE QUESTION',
            'help': 'NEW UNIQUE QUESTION HELP',
            'required': 5,
            'catalog': 0,
            'widget': 'radiobox',
            'display_fields': ['name'],
            'children': '{}',
            'schema': ''
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
            'text': 'NEW UNIQUE QUESTION',
            'help': 'NEW UNIQUE QUESTION HELP',
            'required': 0,
            'catalog': 0,
            'display_fields': ['name'],
            'children': '{}',
            'schema': ''
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
            'text': 'NEW UNIQUE QUESTION',
            'help': 'NEW UNIQUE QUESTION HELP',
            'required': 0,
            'widget': 'radiobox',
            'display_fields': ['name'],
            'children': '{}',
            'schema': ''
        }

        self.client.login(username=user.username, password='test')
        resp = self.client.post(url, data=data)
        resp_str = str(resp.content)

        self.assertEqual(resp.status_code, 200)
        self.assertFalse(resp_str.isdigit())

   
class UniqueSelectionQuestionViewRespTest(QuestionViewRespTest):
    url = 'report_builder:unique_selection_resp'
    
    def setUp(self):
        question_data = {
                'display_fields': ['name'],
                'catalog': '0', 
                'widget': 'radiobox',
                'children': '{}', 
                'schema': ''
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
        question = Question.objects.create(
            report=report,
            class_to_load='unique_selection_question',
            text='NEW UNIQUE QUESTION',
            help='NEW UNIQUE QUESTION HELP',
            answer_options=json.dumps(question_data),
            required=Question.OPTIONAL
        )
        report.question_set.add(question)
        project = Project.objects.create(
            description='Test Project',
            content_type=ContentType.objects.first(),
            object_id=0
        )
        ReportByProject.objects.create(
            report=report,
            start_date=datetime.date.today(),
            submit_date=datetime.date.today() + datetime.timedelta(days=30),
            project=project
        )
        Answer.objects.create(
            user= User.objects.first(),
            report= ReportByProject.objects.first(),
            question=question,
            text= '1',
            annotation= 'Answer test annotation',
            display_text= 'Santa Ana'
        )
        City.objects.create(code='SA',name='Santa Ana',location='San Jose')
        City.objects.create(code='WA',name='Washington',location='New York')
        Country.objects.create(code='CR',name='Costa Rica',capital='San Jose')
        Country.objects.create(code='US',name='Estados Unidos',capital='Washington')
        
    def test_post_create_with_correct_arguments_with_login(self):
        user = User.objects.first()
        report = Report.objects.first()
        question = Question.objects.first()

        url = reverse(self.url, kwargs={
            'report_pk': report.pk,
            'question_pk': question.pk
        })

        data = {
            'text': '1',
        }

        self.client.login(username=user.username, password='test')
        resp = self.client.post(url, data=data)

        new_answer = Answer.objects.last()

        self.assertEqual(resp.status_code, 200)
        self.assertEqual(int(resp.content), int(new_answer.pk))
        self.assertEqual(new_answer.text, '1')
        self.assertEqual(new_answer.display_text, 'Santa Ana')
        
    def test_post_update_with_correct_arguments_with_login(self):
        user = User.objects.first()
        report = Report.objects.first()
        question = Question.objects.first()
        answer = Answer.objects.last()
        
        url = reverse(self.url, kwargs={
            'report_pk': report.pk,
            'question_pk': question.pk
        })
        data = {
            'text': '2',
        }

        self.client.login(username=user.username, password='test')
        resp = self.client.post(url, data=data)

        new_answer = Answer.objects.last()

        self.assertEqual(resp.status_code, 200)
        self.assertEqual(answer.pk, new_answer.pk)
        self.assertEqual(int(resp.content), int(new_answer.pk))
        self.assertEqual(new_answer.text, '2')
        self.assertEqual(new_answer.display_text, 'Washington')

    def test_post_create_with_incorrect_arguments_with_login(self):
        user = User.objects.first()
        report = Report.objects.first()
        question = Question.objects.first()

        url = reverse(self.url, kwargs={
            'report_pk': report.pk,
            'question_pk': question.pk
        })

        data = {
            'text': '3',
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
            'text': 'text',
        }

        self.client.login(username=user.username, password='test')
        resp = self.client.post(url, data=data)
        resp_str = str(resp.content)

        self.assertEqual(resp.status_code, 200)
        self.assertFalse(resp_str.isdigit())
        
    def test_post_create_with_incomplete_arguments_with_login(self):
        user = User.objects.first()
        report = Report.objects.first()
        question = Question.objects.first()

        url = reverse(self.url, kwargs={
            'report_pk': report.pk,
            'question_pk': question.pk
        })

        data = {
            'text': '',
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
            
        }

        self.client.login(username=user.username, password='test')
        resp = self.client.post(url, data=data)
        resp_str = str(resp.content)

        self.assertEqual(resp.status_code, 200)
        self.assertFalse(resp_str.isdigit())

class UniqueSelectionQuestionFormTest(QuestionFormTest):
    '''
        Override and extend your tests here
    '''
    pass