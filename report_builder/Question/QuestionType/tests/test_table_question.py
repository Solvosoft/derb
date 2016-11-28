from django.contrib.auth.models import User
from django.urls import reverse

from report_builder.Question.tests import QuestionViewAdminTest, QuestionViewRespTest
from report_builder.Question.tests import QuestionFormTest

from report_builder.models import Question, Answer, Report, ReportByProject


class TableQuestionViewAdminTest(QuestionViewAdminTest):
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
            'answer_options': '{\"catalog\": [\"0\"], \"displays\": [\"code\", \"name\", \"location\"], \"headers\": [\"Code of your city?\", \"Name of your city?\", \"Where is located?\"]}',
            'children': 'test'
        }

        self.client.login(username=user.username, password='test')
        resp = self.client.post(url, data=data)

        new_question = Question.objects.last()

        self.assertEqual(resp.status_code, 200)
        self.assertEqual(new_question.text, 'NEW TABLE QUESTION')
        self.assertEqual(new_question.help, 'NEW TABLE QUESTION HELP')
        self.assertEqual(new_question.required, 0)
        self.assertEqual(new_question.answer_options,'{\"catalog\": [\"0\"], \"displays\": [\"code\", \"name\", \"location\"], \"headers\": [\"Code of your city?\", \"Name of your city?\", \"Where is located?\"]}')

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
            'required': 1,
            'answer_options': '{\"catalog\": [\"0\"], \"displays\": [\"code\", \"name\", \"location\", \"code\"], \"headers\": [\"Code of your city?\", \"Name of your city?\", \"Where is located?\", \"Repeat code\"]}',
            'children': 'test'
        }

        self.client.login(username=user.username, password='test')
        resp = self.client.post(url, data=data)

        new_question = Question.objects.last()

        self.assertEqual(resp.status_code, 200)
        self.assertEqual(new_question.text, 'NEW TABLE QUESTION')
        self.assertEqual(new_question.help, 'NEW TABLE QUESTION HELP')
        self.assertEqual(new_question.required, 1)
        self.assertEqual(new_question.answer_options, '{\"catalog\": [\"0\"], \"displays\": [\"code\", \"name\", \"location\", \"code\"], \"headers\": [\"Code of your city?\", \"Name of your city?\", \"Where is located?\", \"Repeat code\"]}')

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
            'answer_options': '{\"catalog\": [\"0\"], \"displays\": [\"capital\"], \"headers\": [\"Code of your city?\"]}',
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
            'answer_options': '{\"catalog\": [\"0\"], \"displays\": [\"code\", \"name\", \"location\", \"code\"], \"headers\": [\"Code of your city?\", \"Name of your city?\", \"Where is located?\", \"Repeat code\"]}',
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
            'answer_options': '{\"catalog\": [\"0\"], \"displays\": [\"code\", \"name\", \"location\"], \"headers\": [\"Code of your city?\", \"Name of your city?\", \"Where is located?\"]}',
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

class TableQuestionViewRespTest(QuestionViewRespTest):
    def test_post_create_with_correct_arguments_with_login(self):
        user = User.objects.first()
        report = Report.objects.first()
        question = Question.objects.first()

        url = reverse(self.url, kwargs={
            'report_pk': report.pk,
            'question_pk': question.pk
        })

        data = {
            'text': "[('display_field_0', '0'), ('display_field_1', '0'), ('display_field_2', '0')]",
            'annotation': 'Answer test annotation',
            'display_text': 'Code of your city?: SA Name of your city?: Santa Ana Where is located?: San Jose'
        }

        self.client.login(username=user.username, password='test')
        resp = self.client.post(url, data=data)

        new_answer = Answer.objects.last()

        self.assertEqual(resp.status_code, 200)
        self.assertEqual(int(resp.content), int(new_answer.pk))
        self.assertEqual(new_answer.text, "[('display_field_0', '0'), ('display_field_1', '0'), ('display_field_2', '0')]")
        self.assertEqual(new_answer.annotation, 'Answer test annotation')
        self.assertEqual(new_answer.display_text, 'Code of your city?: SA Name of your city?: Santa Ana Where is located?: San Jose')

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
            'text': "[('display_field_0', '1'), ('display_field_1', '1'), ('display_field_2', '1')]",
            'annotation': 'New answer test annotation',
            'display_text': 'Code of your city?: EZ Name of your city?: Escazu Where is located?: San Jose'
        }

        self.client.login(username=user.username, password='test')
        resp = self.client.post(url, data=data)

        new_answer = Answer.objects.last()

        self.assertEqual(resp.status_code, 200)
        self.assertEqual(answer.pk, new_answer.pk)
        self.assertEqual(int(resp.content), int(new_answer.pk))
        self.assertEqual(new_answer.text, "[('display_field_0', '1'), ('display_field_1', '1'), ('display_field_2', '1')]")
        self.assertEqual(new_answer.annotation, 'New answer test annotation')
        self.assertEqual(new_answer.display_text, 'Code of your city?: EZ Name of your city?: Escazu Where is located?: San Jose')

    def test_post_create_with_incorrect_arguments_with_login(self):
        '''
        It is incorrrect, because the options in "text" whit "1" does not correspond to the answers in display_text
        '''
        user = User.objects.first()
        report = Report.objects.first()
        question = Question.objects.first()

        url = reverse(self.url, kwargs={
            'report_pk': report.pk,
            'question_pk': question.pk
        })

        data = {
            'text': "[('display_field_0', '1'), ('display_field_1', '1'), ('display_field_2', '1')]",
            'annotation': 'Answer test annotation',
            'display_text': 'Code of your city?: SA Name of your city?: Santa Ana Where is located?: San Jose'
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
            'display_text': 'Code of your city?: SA Name of your city?: Santa Ana Where is located?: San Jose'
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
            'text': "[('display_field_0', '0'), ('display_field_1', '0'), ('display_field_2', '0')]",
            'annotation': 'Answer test annotation',
        }

        self.client.login(username=user.username, password='test')
        resp = self.client.post(url, data=data)

        self.assertEqual(resp.status_code, 302)


class TableQuestionFormTest(QuestionFormTest):
    '''
        Override and extend your tests here
    '''
    pass