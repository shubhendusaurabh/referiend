from django.conf import settings
from django.core.urlresolvers import reverse


def core_values(request):
    '''Stick handy data everywhere'''

    data = {
            'SITE_TITLE': getattr(settings, 'SITE_TITLE', 'Referiend'),
            'FRAMEWORK_TITLE': getattr(settings, 'FRAMEWORK_TITLE', 'Django'),
        }
    return data

def current_path(request):
    '''Adds the path of the current page to template context except logout page
    Allow to redirect back to the page user was visiting before loggin in
    '''
    context = {}
    if request.path.strip() != reverse('account_logout'):
        context['current_path'] = request.path
    return context
