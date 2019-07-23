
class ProjectInterface(object):

    def project_code(self):
        '''
            Return de project identification code, this can be a model pk or something unique. 
            :rtype: str
        '''
        pass

    def project_name(self):
        '''
            Return the project name
        '''
        pass

    def consultants_queryset(self):
        '''
            Return a queryset with project consultant as django user  
            (can see the project but not fill answers)
        '''
        pass

    def project_consultants(self):
        '''
            Return a list of user name of consultants
        '''
        pass

    def project_life_dates(self):
        '''
            Return a tuple with start_date and end_date seting the validity of 
            project.
            Also can return None if project have not date limits
        '''
        pass

    def organization(self):
        '''
            Return the organization group where the project is 
            (like departament name, or company unit, or project work area)
        '''
        pass

    def get_projects_by_responsable(self, user, responsable=None):
        '''
            Return a list of project ids where user is responsabe or consultant

            If responsable = True then return only projects where user is responsable
            If responsable = False then return only projects where user is consultant
            If responsable = None then return all projects where user is inserted
            as responsable or consultant

            This funtion returns unique identification, like pks ej. [20, 61, 44]
        '''
        pass

    def get_project_by_reviewer(self, user):
        '''
            Return a list of project ids where user is reviewer
            ej. [20, 61, 44]
        '''
        pass

    def get_project_by_criteria(self, criteria):
        '''
            Return a list of project ids that match with the criteria
            ej. [20, 61, 44]
        '''
        pass

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
        pass
