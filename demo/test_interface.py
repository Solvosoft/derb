from django.contrib.contenttypes.models import ContentType

from report_builder.Project_Wrapper.project_interface import ProjectInterface


class TestProjectInterface(ProjectInterface):
    def project_code(self):
        '''
            Return de project identification code, this can be a model pk or something unique. 
            :rtype: str
        '''
        return str(self.pk)

    def project_name(self):
        '''
            Return the project name
        '''
        return self.name

    def consultants_queryset(self):
        '''
            Return a queryset with project consultant as django user  
            (can see the project but not fill answers)
        '''
        return User.objects.filter(pk=self.user.pk)

    def project_consultants(self):
        '''
            Return a list of user name of consultants
        '''
        return [self.user.username]

    def project_life_dates(self):
        '''
            Return a tuple with start_date and end_date seting the validity of 
            project.
            Be aware of timezone dates
            Also can return None if project have not date limits
        '''
        return

    def organization(self):
        '''
            Return the organization group where the project is 
            (like departament name, or company unit, or project work area)
        '''
        return "Organization Bingo"

    def get_projects_by_responsable(self, user, responsable=None):
        '''
            Return a list of project ids where user is responsabe or consultant

            If responsable = True then return only projects where user is responsable
            If responsable = False then return only projects where user is consultant
            If responsable = None then return all projects where user is inserted
            as responsable or consultant

            This funtion returns unique identification, like pks ej. [20, 61, 44]
        '''
        cc = ContentType.objects.get(
            app_label='report_builder', model='reportbyproject')
        klass = cc.model_class()
        return [t.project.object_id for t in klass.objects.filter(
            report__type__app_name='demo', report__type__name='projecttest')]

    def get_project_by_reviewer(self, user):
        '''
            Return a list of project ids where user is reviewer
            ej. [20, 61, 44]
        '''
        cc = ContentType.objects.get(
            app_label='report_builder', model='reportbyproject')
        klass = cc.model_class()
        return [t.project.object_id for t in klass.objects.filter(
            report__type__app_name='demo', report__type__name='projecttest')]

    def get_project_by_criteria(self, criteria):
        '''
            Return a list of project ids that match with the criteria
            ej. [20, 61, 44]
        '''
        cc = ContentType.objects.get(
            app_label='report_builder', model='reportbyproject')
        klass = cc.model_class()

        proys = [t.project.object_id for t in klass.objects.filter(
            report__type__app_name='demo', report__type__name='projecttest')]
        tam = len(proys)
        tam_r = tam
        mod_tam = tam % 3
        parte = tam
        if mod_tam:
            tam_r = tam_r - mod_tam
        parte = tam_r / 3

        if criteria == 1:
            return proys[0:parte]
        elif criteria == 2:
            return proys[parte:parte*2]
        elif criteria == 3:
            return proys[parte*2:parte*3+mod_tam]

        return proys

    def get_criteria(self, exclude=None,  solo_self=None):
        '''
            Return the allocation criteria to project filter.
            see :func:`get_project_by_criteria`.

            It's a list of dictionaries like:

            .. code:: python

                [ {
                    'pk': 'pk',
                    'description': 'description'
                }, ]

            Arguments:
                exclude: List of project ids that are know or is not required to be returned
                solo_self: If it's passed, only return the criteria that are part of project  
        '''
        return [{
                'pk': 1,
                'description': "primer criterio para test"
                }, {
                'pk': 2,
                'description': "segundo criterio para test"
                },
                {
                'pk': 3,
                'description': "tercer criterio para test"
                }]
