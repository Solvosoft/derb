from django.contrib.auth.models import User
from django.urls import reverse

from report_builder.Question.tests import QuestionViewAdminTest, QuestionViewRespTest
from report_builder.Question.tests import QuestionFormTest

from report_builder.models import Question, Answer, Report, ReportByProject


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
            'help': 'NEW UNIQUE QUESTION HELP',
            'required': 5,
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
            'required': 0,
            'answer_options': '{\"display_fields\": [\"name\", \"location\"], \"catalog\": [\"1\"]}',
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
        self.assertEqual(new_answer.text, '0')
        self.assertEqual(new_answer.annotation, 'Answer test annotation')

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


    def test_post_create_with_incorrect_arguments_with_login(self):
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