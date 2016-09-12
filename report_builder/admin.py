from django.contrib import admin
from report_builder.models import Project
from report_builder.models import ReportType
from report_builder.models import Report
from report_builder.models import ReportByProject
from report_builder.models import Reviewer
from report_builder.models import Question
from report_builder.models import Answer
from report_builder.models import Observation

class ProjectAdmin(admin.ModelAdmin):
    search_fields = ('description', 'object_id')
    list_display = ('description',)

class ReportTypeAdmin(admin.ModelAdmin):
    list_display = ('app_name', 'name', 'type')

class ReportAdmin(admin.ModelAdmin):
    list_display = ('name', 'opening_date')

class ReportByProjectAdmin(admin.ModelAdmin):
    search_fields = ('project__description', 'project__object_id')
    list_display = ('project', 'start_date', 'submit_date', 'state', 'make_another')

class ReviewerAdmin(admin.ModelAdmin):
    list_display = ('user', 'order', 'state')
    ordering = ('order',)

class QuestionAdmin(admin.ModelAdmin):
    list_filter = ('report',)

class AnswerAdmin(admin.ModelAdmin):
    list_display = ('user', 'report', 'question')
    filter = ('question__report')

class ObservationAdmin(admin.ModelAdmin):
    raw_id_fields = ('reviewer', 'answer')


admin.site.register(Project, ProjectAdmin)
admin.site.register(ReportType, ReportTypeAdmin)
admin.site.register(Report, ReportAdmin)
admin.site.register(ReportByProject, ReportByProjectAdmin)
admin.site.register(Reviewer, ReviewerAdmin)
admin.site.register(Question, QuestionAdmin)
admin.site.register(Answer, AnswerAdmin)
admin.site.register(Observation, ObservationAdmin)