import random
from HTMLParser import HTMLParser

from django.utils.encoding import python_2_unicode_compatible

from report_builder.encoding import _st


@python_2_unicode_compatible
class KeyHandler(HTMLParser):
    '''
        TODO: docstring
    '''

    def __init__(self):
        self.static_text = ''
        self.dynamic_text = {}
        self.dynamic_text_str = {}
        self.active_key = None
        HTMLParser.__init__(self)

    def get_hashid(self):
        random_number = str(random.randint(500, 10000))
        while random_number in self.dynamic_text:
            random_number = str(random.randint(500, 10000))
        return random_number

    def get_attrs(self, attrs):
        '''
             The parser returns the attributes like [(key, value), (key, value), ]
             This functions convert them into key=value
         '''
        return_value = ''
        for key, value in attrs:
            if value:
                return_value += ' ' + key + '="' + value + '"'

        return return_value

    def handle_starttag(self, tag, attrs):
        ''' Called every time an HTML tag is open '''
        if tag == 'tr' or tag == 'li':
            self.active_key = self.get_hashid()
            self.dynamic_text[self.active_key] = ''
            self.dynamic_text_str[self.active_key] = ''
            self.static_text += ' %(' + self.active_key + ')s '

        if self.active_key:
            self.dynamic_text[self.active_key] += '<' + tag + self.get_attrs(attrs) + '>'
        else:
            self.static_text += '<' + tag + self.get_attrs(attrs) + '>'

    def handle_endtag(self, tag):
        ''' Called every time an HTML tag is closed '''
        if self.active_key:
            self.dynamic_text[self.active_key] += '</' + tag + '>'
        else:
            self.static_text += '</' + tag + '>'

        if tag == 'tr' or tag == 'li':
            self.dynamic_active_text = False
            self.active_key = False

    def handle_data(self, data):
        ''' Called with the HTML content data'''
        if self.active_key:
            self.dynamic_text[self.active_key] += data
        else:
            self.static_text += data

    def __str__(self):
        '''
            Returns the parsed object representation
            If dynamic applies keys sustitution
        '''
        return _st(self.static_text % self.dynamic_text_str)

    def apply_keys(self, keys):
        '''
            TODO: docstring
        '''
        for key in self.dynamic_text:
            a = self.dynamic_text[key]
            b = self.dynamic_text[key] % keys
            if a != b:
                self.dynamic_text_str[key] += b

            if not '%(' in self.dynamic_text[key]:
                self.dynamic_text_str[key] = self.dynamic_text[key]

        for key in self.dynamic_text:
            keys[key] = '%(' + key + ')s'

        self.static_text = self.static_text % keys

    def is_dynamic(self):
        ''' Returns True if the objects is dynamic (contains the tr or li tags), False otherwise'''
        return self.dynamic_text != {}
