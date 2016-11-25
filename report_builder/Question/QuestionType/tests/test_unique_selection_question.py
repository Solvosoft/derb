from django.contrib.auth.models import User
from django.urls import reverse

from report_builder.Question.tests import QuestionViewAdminTest, QuestionViewRespTest
from report_builder.Question.tests import QuestionFormTest

from report_builder.models import Report, Question


class UniqueSelectionQuestionViewAdminTest(QuestionViewAdminTest):
    
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

    def test_post_create_with_incorrect_arguments_with_login(self):
        user = User.objects.first()
        report = Report.objects.first()
        url = reverse(self.url, kwargs={
            'report_pk': report.pk
        })
        data = {
            'text': 'NEW UNIQUE QUESTION',
            'help': '',
            'required': 5,
            'answer_options': '',
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
            'help': 'NEW UNIQUE QUESTION HELP',
            'required': 6,
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
            'answer_options': '{\"display_fields\": [\"name\", \"capital\"], \"catalog\": [\"1\"]}',
            'children': 'test'
        }

        self.client.login(username=user.username, password='test')
        resp = self.client.post(url, data=data)

        self.assertEqual(resp.status_code, 302)

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