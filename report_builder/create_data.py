import random
import datetime
from async_notifications.models import EmailTemplate
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from report_builder import models

PROJECT_NAMES = [
    'Project Manhattan',
    'Sysadmin association project',
    'Operation Know-it-all',
    'dejaVu Project',
    'Hydra Project',
    'Project X'
]

REPORT_NAMES = [
    'Anthropology Department evaluation',
    'Chinese Program',
    'Data Science scholarship',
    'Department of Computer Science reevaluation',
    'Neuroscience Program survey',
    'Program in Latin American and Caribbean Studies',
    'Campus Recreation Services Commission',
    'Faculty Senate reelection',
    'IT department job evaluation',
    'Office of Human Resources examination',
    'Marketing study for the future',
    'High Commander\'s log'
]

QUESTIONS = [
    'How likely is it that you would recommend this company to a friend or colleague?',
    'Overall, how satisfied or dissatisfied are you with our company?',
    'Which of the following words would you use to describe our products? Select all that apply.',
    'How well do our products meet your needs?',
    'How would you rate the quality of the product?',
    'How would you rate the value for money of the product?',
    'How responsive have we been to your questions or concerns about our products?',
    'How long have you been a customer of our company?',
    'How likely are you to purchase any of our products again?',
    'Do you have any other comments, questions, or concerns?',
    'How meaningful is your work?',
    'How challenging is your job?',
    'In a typical week, how often do you feel stressed at work?',
    'How well are you paid for the work you do?',
    'How much do your opinions about work matter to your coworkers?',
    'How realistic are the expectations of your supervisor?',
    'How often do the tasks assigned to you by your supervisor help you grow professionally?',
    'How many opportunities do you have to get promoted where you work?',
    'Are you supervised too much at work, supervised too little, or supervised about the right amount?',
    'Are you satisfied with your employee benefits, neither satisfied nor dissatisfied with them, or dissatisfied with them?',
    'Are you satisfied with your job, neither satisfied nor dissatisfied with it, or dissatisfied with it?',
    'How proud are you of your employer\'s brand?',
    'Do you like your employer, neither like nor dislike them, or dislike them?',
    'How likely are you to look for another job outside the company?',
    'Overall, how would you rate the quality of your customer service experience?',
    'How well did we understand your questions and concerns?',
    'How much time did it take us to address your questions and concerns?',
    'How likely is it that you would recommend this company to a friend or colleague?',
    'Do you have any other comments, questions, or concerns?',
    'What do you like most about our new product?',
    'What changes would most improve our new product?',
    'What do you like most about competing products currently available from other companies?',
    'What changes would most improve competing products currently available from other companies?',
    'What would make you more likely to use our new product?',
    'If our new product were available today, how likely would you be to recommend it to others?',
    'If you are not likely to use our new product, why not?',
    'How important is price to you when choosing this type of company?',
    'Overall, are you satisfied with your experience using our new product, dissatisfied with it, or neither satisfied or dissatisfied with it?',
    'If our new product were available today, how likely would you be to use it instead of competing products currently available from other companies?',
    'What do you like most about our new service?',
    'What changes would most improve our new service?',
    'What do you like most about competing services currently available from other companies?',
    'What changes would most improve competing services currently available from other companies?',
    'If our new company were available today, how likely would you be to recommend it to others?',
    'What would make you more likely to use our new service?',
    'How important is convenience when choosing this type of service?',
    'If you are not likely to use our new service, why not?',
    'Overall, are you satisfied with your experience using our new service, neither satisfied or dissatisfied with it, or dissatisfied with it?',
    'If our new service were available today, how likely would you be to use it instead of competing services currently available from other companies?',
    'How many school-age children do you have (K-12)?',
    'Which elementary school is in your district?',
    'What school(s) does your child/children attend?',
    'My child/children attend(s)',
    'Whom would you like to evaluate?',
    'How likely is it that you would recommend your supervisor to a colleague?',
    'How easy is it to get help from your supervisor when you want it?',
    'How available to employees is your supervisor?',
    'How often does your supervisor give you feedback about your work?',
    'How improved is your performance after getting feedback from your supervisor about your work?',
    'How effective is the training you receive from your supervisor?',
    'How consistently does your supervisor reward employees for good work?',
    'How consistently does your supervisor punish employees for bad work?',
    'How reasonable are the decisions made by your supervisor?',
    'Does your supervisor take too much time to make decisions, too little time, or about the right amount of time?',
    'How often does your supervisor listen to employees\' opinions when making decisions?',
    'How easy is it for employees to disagree with the decisions made by your supervisor?',
    'When you make a mistake, how often does your supervisor respond constructively?',
    'How reliable is your supervisor?',
    'How effectively does your supervisor use company resources?',
    'When someone completes a task especially well, how often does your supervisor acknowledge this success?',
    'How professionally does your supervisor behave?',
    'Overall, are you satisfied with your supervisor, neither satisfied nor dissatisfied with him/her, or dissatisfied with him/her?',
    'Overall, how effective at his job is your supervisor?',
    'What does your supervisor need to do to improve his/her performance?'
]


def create_projects():
    for i in range(0, len(PROJECT_NAMES)):
        models.Project.objects.create(
            description=PROJECT_NAMES[i],
            content_type=random_choice(get_content_types()),
            object_id=i
        )


def create_report_types(max=5):
    for i in range(0, max):
        models.ReportType.objects.create(
            type='report_type_%d' % i,
            app_name='report_builder',
            name='report',
            action_ok=EmailTemplate.objects.create(
                code='ok_report_type_%d' % i, subject='', message=''),
            revision_turn=EmailTemplate.objects.create(
                code='turn_report_type_%d' % i, subject='', message=''),
            responsable_change=EmailTemplate.objects.create(
                code='change_report_type_%d' % i, subject='', message=''),
            report_start=EmailTemplate.objects.create(
                code='start_report_type_%d' % i, subject='', message=''),
            report_end=EmailTemplate.objects.create(
                code='end_report_type_%d' % i, subject='', message='')
        )


def create_reports():
    for i in range(0, len(REPORT_NAMES)):
        models.Report.objects.create(
            type=random_model_object(models.ReportType),
            name=REPORT_NAMES[i],
            template={},
            opening_date=random_future_date()
        )


def create_report_by_projects():
    for i in range(0, len(REPORT_NAMES)):
        start_date = random_future_date()
        models.ReportByProject.objects.create(
            report=models.Report.objects.get(name=REPORT_NAMES[i]),
            start_date=start_date,
            end_date=start_date +
            datetime.timedelta(days=random.randint(0, 10)),
            state=random_choice(models.ReportByProject.STATES)[0],
            project=random_model_object(models.Project)
        )


def create_reviewers(max=3):
    if max > User.objects.count():
        max = User.objects.count()

    for i in range(0, max):
        models.Reviewer.objects.create(
            user=random_model_object(User),
            report=random_model_object(models.ReportByProject),
            order=random_choice(models.REVIEWER_ORDERS)[0]
        )


def create_questions():
    for i in range(0, len(QUESTIONS)):
        models.Question.objects.create(
            report=random_model_object(models.Report),
            class_to_load='derb',
            text=QUESTIONS[i],
            answer_options={},
            required=random_choice(models.Question.REQUIREMENT_TYPE)[0]
        )


def create_data():
    clean_models()
    create_projects()
    create_report_types()
    create_reports()
    create_report_by_projects()
    create_reviewers()
    create_questions()


def clean_models():
    models.Project.objects.all().delete()
    models.ReportType.objects.all().delete()
    models.Report.objects.all().delete()
    models.ReportByProject.objects.all().delete()
    models.Reviewer.objects.all().delete()
    models.Question.objects.all().delete()


def get_content_types():
    return ContentType.objects.filter(app_label='report_builder')


def random_choice(iterable):
    return random.choice(iterable)


def random_model_object(model):
    return model.objects.order_by('?').first()


def random_future_date():
    return datetime.datetime.now() + datetime.timedelta(days=random.randint(1, 10))
