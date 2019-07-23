from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.urlresolvers import reverse
from django.shortcuts import get_object_or_404, redirect
from django.utils import timezone
from django.views.generic.base import TemplateView
from django.views.generic.edit import CreateView
from django.views.generic.list import ListView

from report_builder import registry
from report_builder.Report import RESPONSABLE, get_reports_by_user
from report_builder.forms import NewReportForm
from report_builder.models import RES_SUPPORTED, Report
from report_builder.registry import register_initial_view
from report_builder.shortcuts import copy_report, get_reviewers_by_report, \
    get_reviewers_by_user


class InitialIndexView(LoginRequiredMixin, TemplateView):
    '''
        TODO: docstring
    '''
    template_name = 'initials/index.html'

    def get_context_data(self, **kwargs):
        '''
            Add the views to be shown to the template's context data for the 
            user to see them
        '''
        context = super(InitialIndexView, self).get_context_data(**kwargs)
        context['views'] = self.get_views(**kwargs)
        return context

    def get_views(self, **kwargs):
        '''
            Renders the views that must be shown to the user. Returns a list 
            that contains the view's title and the HTML content to insert into
            the main template
        '''
        return_value = []

        for v in registry.view_list:
            if v[3](self.request, **kwargs):
                view = v[0](self.request, **kwargs)
                view.render()
                return_value.append(
                    {
                        'title': v[1],
                        'content': view.content
                    }
                )
        return return_value


class InitialReviewerView(LoginRequiredMixin, ListView):
    '''
        Initial view for reviewer role.
        Lists the projects that must be reviewed for the reviewer 
        authenticated user
    '''
    template_name = 'initials/initial_reviewer.html'

    def get_queryset(self):
        '''
            TODO: docstring
        '''
        reviewers = get_reviewers_by_user(self.request.user)
        reports = []
        if len(reviewers) > 0:
            for reviewer in reviewers:
                reviewer.report.review_percentage = \
                    calculate_reviewer_list_porcentage(reviewer.report)
                reports.append(reviewer.report)
        return reports


def calculate_reviewer_list_porcentage(report):
    '''
        TODO: docstring
    '''
    reviewers = get_reviewers_by_report(report)
    if len(reviewers) > 0:
        size = len(reviewers) - 1
        levels = reviewers[size].order
        count = 0
        for reviewer in reviewers:
            if reviewer.state == RES_SUPPORTED:
                count += 1
        return int(float(count) / float(levels) * 100)
    else:
        return 0


class InitialTemplateAdminView(LoginRequiredMixin, ListView):
    '''
        Initial view for the template administrator role.
        List all the existing report templates for the authenticated user
    '''
    template_name = 'initials/initial_template_admin.html'

    def get_queryset(self):
        '''
            TODO: docstring
        '''
        if self.request.user.has_perm('derb.template_admin'):
            return Report.objects.all().order_by('-opening_date')
        else:
            return Report.objects.none()

    def get_context_data(self, **kwargs):
        '''
            TODO: docstring
        '''
        context = super(
            InitialTemplateAdminView, self).get_context_data(**kwargs)
        new_object_list = []
        for report in context['object_list']:
            open_reports = (
                report, report.opening_date > timezone.now())
            new_object_list.append(open_reports)
        context['object_list'] = new_object_list
        return context


# FIXME: Move to other file
class NewReportView(LoginRequiredMixin, CreateView):
    '''
        View that allows a new report (template) creation.
        Takes advantage of the generic view for creating objects
    '''
    model = Report
    form_class = NewReportForm
    template_name = 'initials/new_report.html'

    def get_success_url(self):
        '''
            Redirects to the report's edit view, when the report is correctly 
            created and saved in the database with the data retrieved by 
            the user
        '''
        return reverse('report_builder:admin_report', args=[self.object.id])


# FIXME: Move to other file
@login_required
def NewReportTemplate(request, pk):
    '''
         TODO: docstring
    '''
    report = get_object_or_404(Report, pk=pk)
    new = copy_report(report)
    new.save()
    return redirect(reverse('report_builder:admin_report', args=[new.pk]))


def assign_type_porcentage_to_reports(reports):
    '''
        TODO: docstring
    '''
    reps = []
    if len(reports) > 0:
        for report in reports['responsable']:
            report_and_type = {}
            report.review_percentage = calculate_reviewer_list_porcentage(
                report)
            report_and_type['type'] = 'responsable'
            report_and_type['report'] = report
            reps.append(report_and_type)

        for report in reports['collaborator']:
            report_and_type = {}
            report.review_percentage = calculate_reviewer_list_porcentage(
                report)
            report_and_type['type'] = 'collaborator'
            report_and_type['report'] = report
            reps.append(report_and_type)

    return reps


class InitialResponsableView(LoginRequiredMixin, ListView):
    '''
        Initial view for the responsable role. Lists the current projects for
        responsables and collaborators of the project. 
        Takes advantage of the Django generic view for object creation
    '''
    template_name = 'initials/initial_responsable.html'
    all_reports = False  # Only the current reports

    def get_queryset(self):
        '''
            Returns the current reports assigned to the responsable user. Plus, 
            returns the permission and review porcentage added with the 
            function
            :func: `assign_type_porcentage_to_reports`
        '''
        current_reports = get_reports_by_user(
            self.request.user, RESPONSABLE, None, True)
        return assign_type_porcentage_to_reports(current_reports)

    def get_context_data(self, **kwargs):
        context = super(
            InitialResponsableView, self).get_context_data(**kwargs)
        context['all_reports'] = self.all_reports
        context['resp'] = True
        return context


register_initial_view(
    InitialTemplateAdminView.as_view(), "Admin", 0, lambda x: True)
register_initial_view(
    InitialResponsableView.as_view(), "Responsable", 1, lambda x: True)
register_initial_view(
    InitialReviewerView.as_view(), "Review reports", 2, lambda x: True)
