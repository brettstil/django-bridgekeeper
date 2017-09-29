
from django.conf import settings

from .models import Invite


def get_invite_code(request):
    COOKIE_NAME = getattr(
        settings, 'BRIDGEKEEPER_COOKIE_NAME', 'bridgekeeper_invite_code')
    return request.COOKIES.get(COOKIE_NAME)


def get_invite(request):
    invite_code = get_invite_code(request)
    invite = None
    try:
        invite = Invite.objects.get(code=invite_code)
    except Invite.DoesNotExist:
        pass
    return invite
