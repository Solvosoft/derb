"""
    Created 12/07/2016

    @author: jaquer
"""
from __future__ import unicode_literals
from django.utils.encoding import python_2_unicode_compatible

from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.conf import settings
from report_builder import managers
from report_builder.managers import CanReviewManager
from report_builder.managers import ActiveReviewersManager

from django.contrib.postgres.fields import JSONField

from async_notifications.models import EmailTemplate
from django.utils.translation import ugettext_lazy as _

from django.db import models

# Report states
RS_SUBMIT_PENDING = 0
RS_UNSUBMITTED = 1
RS_APROVED = 2
RS_EDITING = 3
RS_CANCELED = 4
RS_REJECTED = 5
RS_REVIEW = 6

# Reviewer states
RES_UNSUPPORTED = 0
RES_SUPPORTED = 1
RES_REVIEW = 2
RES_SYS_SUPPORTED = 3
RES_SYS_UNSUPPORTED = 4

# Reviewer order states
REV_FIRST = 1
REV_SECOND = 2
REV_THIRD = 3
REV_FOURTH = 4
REV_FIFTTH = 5
REV_SIXTH = 6
REV_SEVENTH = 7

# Reviewer orders
REVIEWER_ORDERS = (
    (REV_FIRST, _('First')),
    (REV_SECOND, _('Second')),
    (REV_THIRD, _('Third')),
    (REV_FOURTH, _('Fourth')),
    (REV_FIFTTH, _('Fifth')),
    (REV_SIXTH, _('Sixth')),
    (REV_SEVENTH, _('Seventh'))
)

@python_2_unicode_compatible
class Project(models.Model):
    # TODO: documentation
    description = models.CharField(max_length=500)
    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    def __str__(self):
        return '%s' % self.description

    class Meta:
        verbose_name = _('Project')
        verbose_name_plural = _('Projects')


@python_2_unicode_compatible
class ReportType(models.Model):
    # TODO: documentation
    type = models.TextField()
    app_name = models.SlugField()  # Application to load from
    name = models.SlugField()  # Model to load

    # Email settings

    action_ok = models.ForeignKey(EmailTemplate,
                                  related_name="action_ok")

    revision_turn = models.ForeignKey(
        EmailTemplate, related_name="revision_turn")
    responsable_change = models.ForeignKey(
        EmailTemplate, related_name="responsable_change")

    report_start = models.ForeignKey(
        EmailTemplate, related_name="report_start")

    report_end = models.ForeignKey(
        EmailTemplate, related_name="report_end")

    def __str__(self):
        return '%s' % self.type

    class Meta:
        verbose_name = _('Report type')
        verbose_name_plural = _('Report types')


@python_2_unicode_compatible
class Report(models.Model):
    # TODO: documentation
    DEFAULT_TEMPLATE = [
        {
            "name": "categ0",
            "order": 0,
            "human_name": "General information",
            "subcategories": [
                {
                    "name": "categ0_categ0",
                    "human_name": "General information",
                    "questions": [],
                    "order": 0,
                    "question": []
                }
            ],
            "subcategories_count": 1
        }
    ]

    type = models.ForeignKey(ReportType)
    name = models.CharField(max_length=200)
    template = JSONField(default=DEFAULT_TEMPLATE)
    questions = JSONField(default={})
    opening_date = models.DateField()

    def __str__(self):
        return '%s' % self.name

    class Meta:
        # TODO: permissions
        verbose_name = _('Report')
        verbose_name_plural = _('Reports')


@python_2_unicode_compatible
class ReportByProject(models.Model):
    STATES = (
        (RS_SUBMIT_PENDING, _('Submit pending')),
        (RS_UNSUBMITTED, _('Unsubmitted')),
        (RS_APROVED, _('Aproved')),
        (RS_EDITING, _('Editing')),
        (RS_CANCELED, _('Canceled')),
        (RS_REJECTED, _('Rejected')),
        (RS_REVIEW, _('In review'))
    )
    report = models.ForeignKey(Report)
    start_date = models.DateField(verbose_name=_('Opening date'))
    submit_date = models.DateField(verbose_name=_('Submit date'))
    state = models.SmallIntegerField(choices=STATES,
                                     default=RS_SUBMIT_PENDING)
    project = models.ForeignKey(Project)
    actions = models.TextField(blank=True, null=True)
    review_percentage = models.SmallIntegerField(default=0)
    complete = models.BooleanField(default=False)
    make_another = models.BooleanField(default=False)
    created_automatically = models.BooleanField(default=False)
    creation_date = models.DateField(auto_now=True)
    additional_info = models.TextField(blank=True, null=True)

    objects = models.Manager()
    current = managers.CurrentReportsManager()
    actives = managers.ActiveReportsManager()
    editables = managers.EditableReportsManager()

    # TODO: Managers

    def __str__(self):
        return '%s - %s - %s' % (self.project.description, self.start_date, self.submit_date)

    class Meta:
        # TODO: permissions
        verbose_name = _('Report by project')
        verbose_name_plural = _('Reports by project')


@python_2_unicode_compatible
class Reviewer(models.Model):
    STATES = (
        (RES_UNSUPPORTED, _('Unsupported')),
        (RES_SUPPORTED, _('Supported')),
        (RES_REVIEW, _('In review')),
        (RES_SYS_SUPPORTED, _('Supported by the system')),
        (RES_SYS_UNSUPPORTED, _('Unsupported by the system'))
    )

    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    report = models.ForeignKey(ReportByProject)
    order = models.SmallIntegerField(choices=REVIEWER_ORDERS)
    state = models.SmallIntegerField(choices=STATES, default=RES_UNSUPPORTED)
    active = models.BooleanField(default=True)
    make_observations = models.BooleanField(default=False)
    can_ask = models.BooleanField(default=False)
    can_review = models.BooleanField(default=False)
    assigned_automatically = models.BooleanField(default=False)

    objects = models.Manager()
    review = CanReviewManager()
    actives = ActiveReviewersManager()

    def __str__(self):
        return '%s' % self.user

    # TODO: __repr__

    class Meta:
        verbose_name = _('Reviewer')
        verbose_name_plural = _('Reviewers')


@python_2_unicode_compatible
class Question(models.Model):
    REQUIREMENT_TYPE = (
        (0, _('Optional')),
        (1, _('Required')),
        (2, _('Required by hierarchy'))
    )
    report = models.ForeignKey(Report, null=True)
    class_to_load = models.CharField(max_length=30)
    text = models.TextField()
    help = models.TextField(blank=True)
    answer_options = JSONField(blank=True, null=True)
    required = models.IntegerField(choices=REQUIREMENT_TYPE, default=0)
    order = models.CharField(max_length=10, blank=True)
    auto = models.BooleanField(default=False)

    objects = models.Manager()
    report_only = managers.ReportQuestionsManager()

    def __str__(self):
        return '%s' % self.text

    class Meta:
        verbose_name = _('Question')
        verbose_name_plural = _('Questions')


@python_2_unicode_compatible
class Answer(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    report = models.ForeignKey(ReportByProject, null=True)
    question = models.ForeignKey(Question)
    annotation = models.TextField(blank=True)
    text = models.TextField(blank=True)
    display_text = models.TextField(blank=True)

    def __str__(self):
        return '%s - %s' % (self.user.get_full_name(), self.display_text)

    class Meta:
        verbose_name = _('Answer')
        verbose_name_plural = _('Answers')


@python_2_unicode_compatible
class Observation(models.Model):
    reviewer = models.ForeignKey(Reviewer)
    text = models.TextField()
    context = models.TextField()
    answer = models.ForeignKey(Answer)
    aproved = models.BooleanField(default=False)

    def __str__(self):
        return '%s - %s' % (self.reviewer, self.text)

    class Meta:
        verbose_name = _('Observation')
        verbose_name_plural = _('Observations')


@python_2_unicode_compatible
class RevisionTreeUser(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    order = models.SmallIntegerField(choices=REVIEWER_ORDERS)
    make_observations = models.BooleanField(default=True)
    can_ask = models.BooleanField(default=True)
    can_review = models.BooleanField(default=True)

    def __str__(self):
        return '%s' % self.user

    class Meta:
        verbose_name = _('Revision Tree User')
        verbose_name_plural = _('Revision Tree Users')


@python_2_unicode_compatible
class RevisionTree(models.Model):
    report_type = models.ForeignKey(ReportType)
    assignment_criteria = models.CharField(max_length=100)
    description = models.TextField()
    revision_tree_user = models.ManyToManyField(RevisionTreeUser)

    def __str__(self):
        return '%s' % self.description

    class Meta:
        # TODO: permissions
        verbose_name = _('Revision Tree')
        verbose_name_plural = _('Revision Tree')


# Testing catalogs

@python_2_unicode_compatible
class City(models.Model):
    code = models.CharField(max_length=2)
    name = models.CharField(max_length=255)
    location = models.CharField(max_length=255)

    def __str__(self):
        return '%s' % self.name


@python_2_unicode_compatible
class Country(models.Model):
    code = models.CharField(max_length=2)
    name = models.CharField(max_length=255)
    capital = models.CharField(max_length=255)

    def __str__(self):
        return '%s' % self.name
