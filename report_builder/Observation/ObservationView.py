import random
from django.views.generic.list import ListView
from report_builder.models import Observation
from report_builder.models import Answer
from django.shortcuts import get_object_or_404
from report_builder.shortcuts import get_reportbyproject_questions
from report_builder.shortcuts import get_active_reviewer
from report_builder.models import RES_SUPPORTED, RES_UNSUPPORTED, RS_REVIEW


class ObservationView(ListView):
    # TODO: define template
    template_name = 'observation/base_template.html'
    paginate_by = 1
    model = Observation
    answer = None
    form_number = random.randint(500, 10000)
    make_observations = False
    is_reviewer = False

    def get_queryset(self):
        """
            TODO: docstring
        """
        if self.kwargs['answer_pk'] is not None:
            self.answer = get_object_or_404(Answer, pk=self.kwargs['answer_pk'])
            return Observation.objects.filter(answer=self.answer).order_by('pk')
        else:
            answers = Answer.objects.filter(report__pk=int(self.kwargs['answer_pk']),
                                            question__pk=int(self.kwargs['question_pk']))
            if len(answers) > 0:
                self.kwargs['answer_pk'] = answers.values('pk')[0]['pk']
                return Observation.objects.filter(answer__in=[q['pk'] for q in answers.values('pk')]).order_by('pk')
            return Observation.objects.none()

    def get_context_data(self, **kwargs):
        """
            TODO: docstring
        """
        context = super(ObservationView, self).get_context_data(**kwargs)
        reportbyproject, question = get_reportbyproject_questions(self.kwargs['report_pk'], self.kwargs['question_pk'])
        reviewer = get_active_reviewer(reportbyproj=reportbyproject, user=self.request.user)
        if reviewer is not None:
            self.is_reviewer = True
            self.make_observations = reviewer.make_observations
            if reportbyproject.state != RS_REVIEW or reviewer.state == RES_SUPPORTED or reviewer.state == RES_UNSUPPORTED:
                self.make_observations = False
        else:
            self.is_reviewer = self.make_observations = False
        context['answer'] = self.answer
        context['form_number'] = str(self.form_number)
        context['collapse_number'] = str(random.randint(500, 10000))
        context['report_pk'] = self.kwargs['report_pk']
        context['question_pk'] = self.kwargs['question_pk']
        context['is_reviewer'] = self.is_reviewer
        context['make_observations'] = self.make_observations
        return context
