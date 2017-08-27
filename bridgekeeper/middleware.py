from django.http import HttpResponseRedirect
from django.conf import settings
from django.utils.module_loading import import_string

from .models import Invite


def authenticated(request, view_func, view_args, view_kwargs):
    if request.user.is_authenticated:
        return True


def enable(request, view_func, view_args, view_kwargs):
    ENABLE = getattr(settings, 'BRIDGEKEEPER_ENABLE', True)

    if ENABLE is False:
        return True


def allowed_module(request, view_func, view_args, view_kwargs):
    ALLOWED_MODULES = getattr(
        settings, 'BRIDGEKEEPER_ALLOWED_MODULES', [])
    allowed_modules = [
        'django.contrib.admin.sites',
        'django.contrib.auth.views',
        'django.contrib.staticfiles.views',
        'django.views.static',
    ] + ALLOWED_MODULES

    if view_func.__module__ in allowed_modules:
        return True


def allowed_view(request, view_func, view_args, view_kwargs):
    ALLOWED_VIEWS = getattr(
        settings, 'BRIDGEKEEPER_ALLOWED_VIEWS', [])
    allowed_views = [
        'bridgekeeper.views.invited',
    ] + ALLOWED_VIEWS
    view_module_name = '{}.{}'.format(
        view_func.__module__, view_func.__name__)

    if view_module_name in allowed_views:
        return True


def valid_invite(request, view_func, view_args, view_kwargs):
    COOKIE_KEY = getattr(
        settings, 'BRIDGEKEEPER_COOKIE_NAME', 'bridgekeeper_invite_code')

    invite_code = request.COOKIES.get(COOKIE_KEY, None)
    if not invite_code:
        return False

    try:
        invite = Invite.objects.get(code=invite_code)
    except Invite.DoesNotExist:
        return False

    if not invite.is_valid():
        return False
    else:
        return True


def known_traveler_may_pass(request, view_func, view_args, view_kwargs):
    '''
    Always returns True, for tests and local development.
    '''
    return True


def known_cast_into_gorge(request, view_func, view_args, view_kwargs):
    '''
    Always returns False, for tests and local development.
    '''
    return False


def known_none(request, view_func, view_args, view_kwargs):
    '''
    Always returns None, for tests and local development.
    '''
    return


class BridgekeeperMiddleware(object):

    def __init__(self, get_response):
        self.get_response = get_response
        # One-time configuration and initialization.

    def __call__(self, request):
        # Code to be executed for each request before
        # the view (and later middleware) are called.
        response = self.get_response(request)
        # Code to be executed for each request/response after
        # the view is called.
        return response

    def process_view(self, request, view_func, view_args, view_kwargs):

        # order of questions is important!
        # break questions out so they're testable and pluggable
        QUESTIONS = getattr(
            settings, 'BRIDGEKEEPER_QUESTIONS',
            [
                'bridgekeeper.middleware.authenticated',
                'bridgekeeper.middleware.enable',
                'bridgekeeper.middleware.allowed_module',
                'bridgekeeper.middleware.allowed_view',
                'bridgekeeper.middleware.valid_invite',
            ])

        # "must answer me these questions" "the other side he see"
        for question_str in QUESTIONS:
            question_func = import_string(question_str)
            answer = question_func(
                request, view_func, view_args, view_kwargs)
            if answer is True:
                # explicit yes, traveler may pass
                return
            elif answer is False:
                # explicit no, cast into gorge
                URL_GORGE = getattr(settings, 'BRIDGEKEEPER_URL_GORGE', '/')
                return HttpResponseRedirect(URL_GORGE)
            # no opinion whether traveler may pass
            # continue to next question, if any
