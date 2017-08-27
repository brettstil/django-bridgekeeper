from django.http import HttpResponseRedirect
from django.conf import settings
from django.utils import timezone

from .models import Invite


def invited(request, code):
    URL_INVITED_INVALID = getattr(
        settings, 'BRIDGEKEEPER_URL_INVITED_INVALID', '/')
    URL_INVITED_OK = getattr(
        settings, 'BRIDGEKEEPER_URL_INVITED_OK', '/')
    COOKIE_KEY = getattr(
        settings, 'BRIDGEKEEPER_COOKIE_NAME', 'bridgekeeper_invite_code')

    try:
        invite = Invite.objects.get(code=code)
    except Invite.DoesNotExist:
        return HttpResponseRedirect(URL_INVITED_INVALID)

    if not invite.is_valid():
        return HttpResponseRedirect(URL_INVITED_INVALID)

    response = HttpResponseRedirect(URL_INVITED_OK)

    # https://docs.djangoproject.com/en/1.11/ref/request-response/#django.http.HttpResponse.set_cookie
    # expires should be datetime.datetime object in utc
    expires = None
    if invite.expired and timezone.is_aware(invite.expired):
        expires = timezone.localtime(invite.expired, timezone.utc)

    response.set_cookie(
        COOKIE_KEY, invite.code, expires=expires, httponly=True)

    return response
