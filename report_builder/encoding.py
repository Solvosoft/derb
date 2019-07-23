from django.utils.encoding import smart_text


def _st(text):
    '''
        Build unicode elements according to Django's documentation about UTF-8
        Uses ``smart_text`` by default
    '''
    if type(text) == str:
        try:
            text = text.decode('utf-8')
        except:
            try:
                text = text.decode('iso-8859-1')
            except:
                text = unicode(text, errors='ignore')

    return smart_text(text, encoding='utf-8', strings_only=False,
                      errors='xmlcharset')
