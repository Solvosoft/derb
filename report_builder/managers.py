from datetime import datetime

from django.db import models
from django.utils import timezone


class CanReviewManager(models.Manager):
    def get_queryset(self):
        return super(CanReviewManager, self).get_queryset().filter(
            active=True, can_review=True)


class ActiveReviewersManager(models.Manager):
    def get_queryset(self):
        return super(ActiveReviewersManager, self).get_queryset().filter(
            active=True)


class CurrentReportsManager(models.Manager):
    today = timezone.now()

    def get_queryset(self):
        return super(CurrentReportsManager, self).get_queryset().filter(
            start_date__lte=self.today,
            end_date__gte=self.today). \
            exclude(state__in=(1, 4))


class ActiveReportsManager(models.Manager):
    today = timezone.now()

    def get_queryset(self):
        return super(ActiveReportsManager, self).get_queryset().filter(
            end_date__gte=self.today).exclude(
            state__in=(1, 4))


class EditableReportsManager(models.Manager):
    today = timezone.now()

    def get_queryset(self):
        return super(EditableReportsManager, self).get_queryset().filter(
            end_date__gte=self.today).exclude(
            state__in=(1, 2, 4))


class ReportQuestionsManager(models.Manager):

    def get_queryset(self):
        return super(ReportQuestionsManager, self).get_queryset().filter(
            automatic=False)
