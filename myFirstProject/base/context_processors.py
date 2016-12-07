from django.core.urlresolvers import resolve
from django.utils.translation import ugettext as _

home = (_('Start'), 'home')

breadcrumbs_views = {'home': [home],
                     'index': [(_('Landing'), 'index')],
                     }


def breadcrumbs(request):
    """
    Context processor for include general breadcrumb in the mains views
    :param request:
    :return: dictionary with the breadcrumb for each view
    """
    view_name = resolve(request.path_info).url_name
    if view_name in breadcrumbs_views:
        return {'breadcrumbs': breadcrumbs_views[view_name]}
    return {}
