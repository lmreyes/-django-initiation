import json
import re

from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse
from django.utils.text import slugify
from django.utils.translation import ugettext_lazy as _

from users.models import User
from base.decorators import ajax_required
from .validators import is_password_secure


@ajax_required
def is_field_available(request):
    slug = request.POST.get('slug')
    try:
        user_details = User.objects.get(slug=slug)
        if user_details.user == request.user:
            msg = _('The public url is available.')
            payload = {'success': True, 'msg': str(msg)}
        else:
            msg = _('The public url is taken.')
            payload = {'success': False, 'msg': str(msg)}
    except ObjectDoesNotExist:
        msg = _('The public url is available.')
        payload = {'success': True, 'msg': str(msg)}

    return HttpResponse(json.dumps(payload), content_type='application/json')


@ajax_required
def is_valid_password(request):
    password = request.POST.get('password')
    pattern = re.compile(is_password_secure)
    if pattern.fullmatch(password):
        msg = _('The password is correct.')
        payload = {'success': True, 'msg': str(msg)}
    else:
        msg = _('The password is invalid.')
        payload = {'success': False, 'msg': str(msg)}

    return HttpResponse(json.dumps(payload), content_type='application/json')


def create_slug(detail_user, first_name, last_name):
    slug = slugify("%s-%s" % (first_name, last_name))
    same_slug_query = User.objects.filter(slug=slug).exists()
    index = 1
    needs_numeration = False
    while same_slug_query:
        needs_numeration = True
        same_slug_query = User.objects.filter(slug="%s-%d" % (slug, index)).exists()
        if same_slug_query:
            index += 1
    if needs_numeration:
        detail_user.slug = "%s-%d" % (slug, index)
    else:
        detail_user.slug = slug
    detail_user.save()


