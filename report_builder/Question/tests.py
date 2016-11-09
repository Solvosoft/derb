import datetime

from async_notifications.models import EmailTemplate
from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from report_builder.forms import QuestionForm
from report_builder.models import Report, ReportType, Question


class QuestionViewAdminTest(TestCase):
    url = 'report_builder:base_question_admin'

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
            class_to_load='derb',
            text='Test question text',
            answer_options={},
            required=Question.OPTIONAL
        )

    def test_get_without_arguments(self):
        resp = None
        try:
            url = reverse(self.url)
            resp = self.client.get(url)
        except:
            url = None

        self.assertEqual(url, None)
        self.assertEqual(resp, None)

    def test_get_with_report_pk_without_login(self):
        report = Report.objects.first()
        url = reverse(self.url, kwargs={
            'report_pk': report.pk
        })
        resp = self.client.get(url)

        self.assertEqual(resp.status_code, 302)

    def test_get_with_report_and_question_pk_without_login(self):
        report = Report.objects.first()
        question = Question.objects.first()
        url = reverse(self.url, kwargs={
            'report_pk': report.pk,
            'question_pk': question.pk
        })
        resp = self.client.get(url)

        self.assertEqual(resp.status_code, 302)

    def test_get_with_report_pk_with_login(self):
        user = User.objects.first()
        report = Report.objects.first()
        url = reverse(self.url, kwargs={
            'report_pk': report.pk
        })
        self.client.login(username=user.username, password='test')
        resp = self.client.get(url)

        self.assertEqual(resp.status_code, 200)

    def test_get_with_report_and_question_pk_with_login(self):
        user = User.objects.first()
        report = Report.objects.first()
        question = Question.objects.first()
        url = reverse(self.url, kwargs={
            'report_pk': report.pk,
            'question_pk': question.pk
        })
        self.client.login(username=user.username, password='test')
        resp = self.client.get(url)

        self.assertEqual(resp.status_code, 200)

    def test_post_without_arguments_without_login(self):
        report = Report.objects.first()
        question = Question.objects.first()
        url = reverse(self.url, kwargs={
            'report_pk': report.pk,
            'question_pk': question.pk
        })

        resp = self.client.post(url)

        self.assertEqual(resp.status_code, 302)

    def test_post_with_null_arguments_with_login(self):
        user = User.objects.first()
        report = Report.objects.first()
        url = reverse(self.url, kwargs={
            'report_pk': report.pk
        })
        self.client.login(username=user.username, password='test')
        resp = self.client.post(url)

        self.assertEqual(resp.status_code, 302)

    def test_post_create_with_correct_arguments_with_login(self):
        user = User.objects.first()
        report = Report.objects.first()
        url = reverse(self.url, kwargs={
            'report_pk': report.pk
        })
        data = {
            'text': 'NEW QUESTION TEXT',
            'help': 'NEW QUESTION HELP',
            'required': 0,
            'children': 'test'
        }

        self.client.login(username=user.username, password='test')
        resp = self.client.post(url, data=data)

        new_question = Question.objects.last()

        self.assertEqual(resp.status_code, 200)
        self.assertEqual(new_question.text, 'NEW QUESTION TEXT')
        self.assertEqual(new_question.help, 'NEW QUESTION HELP')
        self.assertEqual(new_question.required, 0)

    def test_post_update_with_correct_arguments_with_login(self):
        user = User.objects.first()
        report = Report.objects.first()
        question = Question.objects.first()
        url = reverse(self.url, kwargs={
            'report_pk': report.pk,
            'question_pk': question.pk
        })
        data = {
            'text': 'NEW QUESTION TEXT',
            'help': 'NEW QUESTION HELP',
            'required': 0,
            'children': 'test'
        }

        self.client.login(username=user.username, password='test')
        resp = self.client.post(url, data=data)

        new_question = Question.objects.last()

        self.assertEqual(resp.status_code, 200)
        self.assertEqual(new_question.text, 'NEW QUESTION TEXT')
        self.assertEqual(new_question.help, 'NEW QUESTION HELP')
        self.assertEqual(new_question.required, 0)

    def test_post_create_with_incorrect_arguments_with_login(self):
        user = User.objects.first()
        report = Report.objects.first()
        url = reverse(self.url, kwargs={
            'report_pk': report.pk
        })
        data = {
            'text': 'NEW QUESTION TEXT',
            'help': 'NEW QUESTION HELP',
            'required': 5,
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
            'text': '',
            'help': 'NEW QUESTION HELP',
            'required': 1,
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
            'text': 'NEW QUESTION TEXT',
            'help': 'NEW QUESTION HELP',
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
            'help': 'NEW QUESTION HELP',
            'required': 1,
            'children': 'test'
        }

        self.client.login(username=user.username, password='test')
        resp = self.client.post(url, data=data)

        self.assertEqual(resp.status_code, 302)


class QuestionFormTest(TestCase):
    def setUp(self):
        QuestionViewAdminTest.setUp(self)

    def test_form_with_correct_data(self):
        data = {
            'text': 'NEW QUESTION TEXT',
            'help': 'NEW QUESTION HELP',
            'required': 0,
            'children': 'test'
        }
        form = QuestionForm(data=data)
        form.save()

        new_question = Question.objects.last()
        self.assertTrue(form.is_valid())
        self.assertEqual(new_question.text, 'NEW QUESTION TEXT')
        self.assertEqual(new_question.help, 'NEW QUESTION HELP')
        self.assertEqual(new_question.required, 0)

    def test_form_with_null_data(self):
        data = {}
        form = QuestionForm(data=data)
        self.assertFalse(form.is_valid())

    def test_form_with_incorrect_data(self):
        data = {
            'text': 'NEW QUESTION TEXT',
            'help': 'NEW QUESTION HELP',
            'required': 7,
            'children': 'test'
        }
        form = QuestionForm(data=data)

        self.assertFalse(form.is_valid())

    def test_form_with_incomplete_data(self):
        data = {
            'help': 'NEW QUESTION HELP',
            'required': 0
        }
        form = QuestionForm(data=data)

        self.assertFalse(form.is_valid())