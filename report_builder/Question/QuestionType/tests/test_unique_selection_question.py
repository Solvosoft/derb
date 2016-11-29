import datetime

from async_notifications.models import EmailTemplate
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
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
            answer_options='{\"display_fields\": [\"name\"], \"catalog\": [\"1\"]}',
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
            'answer_options': '{\"display_fields\": [\"name\"], \"catalog\": [\"1\"]}',
            'children': 'test'
        }

        self.client.login(username=user.username, password='test')
        resp = self.client.post(url, data=data)

        new_question = Question.objects.last()

        self.assertEqual(resp.status_code, 200)
        self.assertEqual(new_question.text, 'NEW UNIQUE QUESTION')
        self.assertEqual(new_question.help, 'NEW UNIQUE QUESTION HELP')
        self.assertEqual(new_question.required, 0)
        self.assertEqual(new_question.answer_options,'{\"display_fields\": [\"name\"], \"catalog\": [\"1\"]}')

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
            'required': 0,
            'answer_options': '{\"display_fields\": [\"name\", \"capital\"], \"catalog\": [\"1\"]}',
            'children': 'test'
        }

        self.client.login(username=user.username, password='test')
        resp = self.client.post(url, data=data)

        new_question = Question.objects.last()

        self.assertEqual(resp.status_code, 200)
        self.assertEqual(new_question.text, 'NEW UNIQUE QUESTION')
        self.assertEqual(new_question.help, 'NEW UNIQUE QUESTION HELP')
        self.assertEqual(new_question.required, 0)
        self.assertEqual(new_question.answer_options,'{\"display_fields\": [\"name\", \"capital\"], \"catalog\": [\"1\"]}')

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
            'answer_options': '{\"display_fields\": [\"name\", \"capital\"], \"catalog\": [\"0\"]}',
            'children': 'test'
        }

        self.client.login(username=user.username, password='test')
        resp = self.client.post(url, data=data)

        self.assertEqual(resp.status_code, 302)

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
            'answer_options': '{\"display_fields\": [\"name\", \"capital\"], \"catalog\": [\"1\"]}',
            'children': 'test'
        }

        self.client.login(username=user.username, password='test')
        resp = self.client.post(url, data=data)

        self.assertEqual(resp.status_code, 302)

    def test_post_create_with_incomplete_arguments_with_login(self):
        user = User.objects.first()
        report = Report.objects.first()
        url = reverse(self.url, kwargs={
            'report_pk': report.pk
        })
        data = {
            'text': 'NEW UNIQUE QUESTION',
            'help': 'NEW UNIQUE QUESTION HELP',
            'children': 'test'
        }

        self.client.login(username=user.username, password='test')
        resp = self.client.post(url, data=data)

        self.assertEqual(resp.status_code, 302)

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
            'children': 'test'
        }

        self.client.login(username=user.username, password='test')
        resp = self.client.post(url, data=data)

        self.assertEqual(resp.status_code, 302)

class UniqueSelectionQuestionViewRespTest(QuestionViewRespTest):
    url = 'report_builder:unique_selection_resp'
    
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
        question = Question.objects.create(
            report=report,
            class_to_load='unique_selection_question',
            text='NEW UNIQUE QUESTION',
            help='NEW UNIQUE QUESTION HELP',
            answer_options='{\"display_fields\": [\"name\"], \"catalog\": [\"1\"]}',
            required=Question.OPTIONAL
        )
        Answer.objects.create(
            user= User.objects.first(),
            report=report,
            question=question,
            text= '1',
            annotation= 'Answer test annotation',
            display_text= 'Costa Rica'
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
            'annotation': 'Answer test annotation',
            'display_text': 'Costa Rica'
        }

        self.client.login(username=user.username, password='test')
        resp = self.client.post(url, data=data)

        new_answer = Answer.objects.last()

        self.assertEqual(resp.status_code, 200)
        self.assertEqual(int(resp.content), int(new_answer.pk))
        self.assertEqual(new_answer.text, '1')
        self.assertEqual(new_answer.annotation, 'Answer test annotation')
        self.assertEqual(new_answer.display_text, 'Costa Rica')

    def test_post_update_with_correct_arguments_with_login(self):
        user = User.objects.first()
        report = Report.objects.first()
        question = Question.objects.first()
        reportbyproj = ReportByProject.objects.first()
        answer = Answer.objects.create(
            user=user,
            report=reportbyproj,
            question=question,
            annotation='test annotation',
            text='test text',
            display_text='test display text'
        )


        url = reverse(self.url, kwargs={
            'report_pk': report.pk,
            'question_pk': question.pk
        })
        data = {
            'text': '1',
            'annotation': 'New answer test annotation',
            'display_text': 'Costa Rica'
        }

        self.client.login(username=user.username, password='test')
        resp = self.client.post(url, data=data)

        new_answer = Answer.objects.last()

        self.assertEqual(resp.status_code, 200)
        self.assertEqual(answer.pk, new_answer.pk)
        self.assertEqual(int(resp.content), int(new_answer.pk))
        self.assertEqual(new_answer.text, '1')
        self.assertEqual(new_answer.annotation, 'New answer test annotation')
        self.assertEqual(new_answer.display_text, 'Costa Rica')

    def test_post_create_with_incorrect_arguments_with_login(self):
        '''
        It is incorrrect, because "text :1" does not correspond to "España"
        '''
        user = User.objects.first()
        report = Report.objects.first()
        question = Question.objects.first()

        url = reverse(self.url, kwargs={
            'report_pk': report.pk,
            'question_pk': question.pk
        })

        data = {
            'text': '1',
            'annotation': 'Answer test annotation',
            'display_text': 'España'
        }

        self.client.login(username=user.username, password='test')
        resp = self.client.post(url, data=data)

        self.assertEqual(resp.status_code, 302)

    def test_post_update_with_incorrect_arguments_with_login(self):
        '''
        It is incorrrect, because "text :0" does not correspond to "Costa Rica"
        '''
        user = User.objects.first()
        report = Report.objects.first()
        question = Question.objects.first()
        reportbyproj = ReportByProject.objects.first()
        answer = Answer.objects.create(
            user=user,
            report=reportbyproj,
            question=question,
            annotation='test annotation',
            text='test text',
            display_text='test display text'
        )

        url = reverse(self.url, kwargs={
            'report_pk': report.pk,
            'question_pk': question.pk
        })
        data = {
            'text': '0',
            'annotation': 'New answer test annotation',
            'display_text': 'Costa Rica'
        }

        self.client.login(username=user.username, password='test')
        resp = self.client.post(url, data=data)

        self.assertEqual(resp.status_code, 302)

    def test_post_create_with_incomplete_arguments_with_login(self):
        user = User.objects.first()
        report = Report.objects.first()
        question = Question.objects.first()

        url = reverse(self.url, kwargs={
            'report_pk': report.pk,
            'question_pk': question.pk
        })

        data = {
            'annotation': 'Answer test annotation',
            'display_text': 'Costa Rica'
        }

        self.client.login(username=user.username, password='test')
        resp = self.client.post(url, data=data)

        self.assertEqual(resp.status_code, 302)

    def test_post_update_with_incomplete_arguments_with_login(self):
        user = User.objects.first()
        report = Report.objects.first()
        question = Question.objects.first()
        reportbyproj = ReportByProject.objects.first()
        answer = Answer.objects.create(
            user=user,
            report=reportbyproj,
            question=question,
            annotation='test annotation',
            text='test text',
            display_text='test display text'
        )

        url = reverse(self.url, kwargs={
            'report_pk': report.pk,
            'question_pk': question.pk
        })
        data = {
            'text': '1',
            'annotation': 'Answer test annotation',
        }

        self.client.login(username=user.username, password='test')
        resp = self.client.post(url, data=data)

        self.assertEqual(resp.status_code, 302)

class UniqueSelectionQuestionFormTest(QuestionFormTest):
    '''
        Override and extend your tests here
    '''
    pass