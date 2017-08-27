import datetime

from django.test import TestCase, override_settings
from django.http import HttpResponseRedirect
from django.contrib.auth.models import AnonymousUser
from django.utils import timezone

from unittest.mock import Mock

from ..middleware import (
    BridgekeeperMiddleware, known_traveler_may_pass, known_cast_into_gorge,
    known_none, authenticated, enable, allowed_module,
    allowed_view, valid_invite,
)
from ..models import Invite


class MiddlewareTestCase(TestCase):

    def setUp(self):
        self.middleware = BridgekeeperMiddleware(get_response=Mock())
        self.request = Mock()
        self.view = Mock()

    @override_settings(
        BRIDGEKEEPER_URL_GORGE='/gorge/',
        BRIDGEKEEPER_QUESTIONS=[
            'bridgekeeper.middleware.known_cast_into_gorge',
        ])
    def test_questions_loop_cast_into_gorge(self):
        response = self.middleware.process_view(
            self.request, self.view, [], {})
        self.assertTrue(isinstance(response, HttpResponseRedirect))
        self.assertEqual(response.url, '/gorge/')

    @override_settings(
        BRIDGEKEEPER_URL_GORGE='/gorge/',
        BRIDGEKEEPER_QUESTIONS=[
            'bridgekeeper.middleware.known_none',
            'bridgekeeper.middleware.known_none',
            'bridgekeeper.middleware.known_cast_into_gorge',
        ])
    def test_questions_loop_cast_into_gorge_after_none(self):
        response = self.middleware.process_view(
            self.request, self.view, [], {})
        self.assertTrue(isinstance(response, HttpResponseRedirect))
        self.assertEqual(response.url, '/gorge/')

    @override_settings(
        BRIDGEKEEPER_QUESTIONS=[
            'bridgekeeper.middleware.known_traveler_may_pass',
        ])
    def test_questions_loop_user_may_pass(self):
        self.assertIsNone(self.middleware.process_view(
            self.request, self.view, [], {}))

    @override_settings(
        BRIDGEKEEPER_QUESTIONS=[
            'bridgekeeper.middleware.known_traveler_may_pass',
            'bridgekeeper.middleware.known_cast_into_gorge',
            'bridgekeeper.middleware.known_cast_into_gorge',
        ])
    def test_questions_loop_user_may_pass_before_gorge(self):
        self.assertIsNone(self.middleware.process_view(
            self.request, self.view, [], {}))

    @override_settings(
        BRIDGEKEEPER_QUESTIONS=[
            'bridgekeeper.middleware.known_none',
        ])
    def test_questions_loop_none(self):
        self.assertIsNone(self.middleware.process_view(
            self.request, self.view, [], {}))


class QuestionsTestCase(TestCase):

    def setUp(self):
        self.middleware = BridgekeeperMiddleware(get_response=Mock())
        self.request = Mock()
        self.view = Mock()

    def test_known(self):
        self.assertTrue(known_traveler_may_pass(
            self.request, self.view, [], {}))
        self.assertFalse(known_cast_into_gorge(
            self.request, self.view, [], {}))
        self.assertIsNone(known_none(self.request, self.view, [], {}))

    def test_user_anonymous_none(self):
        self.request.user = AnonymousUser()
        self.assertIsNone(authenticated(self.request, self.view, [], {}))

    def test_user_authenticated_may_pass(self):
        self.request.user = Mock()
        self.request.user.authenticated = True
        self.assertTrue(authenticated(self.request, self.view, [], {}))

    @override_settings(BRIDGEKEEPER_ENABLE=False)
    def test_settings_enable_false_may_pass(self):
        self.assertTrue(enable(self.request, self.view, [], {}))

    @override_settings(BRIDGEKEEPER_ENABLE=True)
    def test_settings_enable_true_none(self):
        self.assertIsNone(enable(self.request, self.view, [], {}))

    @override_settings(BRIDGEKEEPER_ALLOWED_MODULES=['camelot'])
    def test_allowed_module_may_pass(self):
        self.view.__module__ = 'camelot'
        self.assertTrue(allowed_module(self.request, self.view, [], {}))

    @override_settings(BRIDGEKEEPER_ALLOWED_MODULES=['camelot'])
    def test_not_in_allowed_module_none(self):
        self.view.__module__ = 'roundtable'
        self.assertIsNone(allowed_module(self.request, self.view, [], {}))

    @override_settings(BRIDGEKEEPER_ALLOWED_VIEWS=['camelot.views.roundtable'])
    def test_allowed_view_may_pass(self):
        self.view.__module__ = 'camelot.views'
        self.view.__name__ = 'roundtable'
        self.assertTrue(allowed_view(self.request, self.view, [], {}))

    @override_settings(BRIDGEKEEPER_ALLOWED_VIEWS=['camelot.views.roundtable'])
    def test_not_in_allowed_view_none(self):
        self.view.__module__ = 'camelot.views'
        self.view.__name__ = 'knights'
        self.assertIsNone(allowed_view(self.request, self.view, [], {}))

    @override_settings(BRIDGEKEEPER_COOKIE_NAME='invite_code')
    def test_valid_invite_may_pass(self):
        invite = Invite.objects.create()
        self.request.COOKIES = {'invite_code': invite.code}
        self.assertTrue(valid_invite(self.request, self.view, [], {}))

    @override_settings(BRIDGEKEEPER_COOKIE_NAME='invite_code')
    def test_expired_invite_code_gorge(self):
        expired = timezone.now() - datetime.timedelta(days=1)
        invite = Invite.objects.create(expired=expired)
        self.request.COOKIES = {'invite_code': invite.code}
        self.assertFalse(valid_invite(self.request, self.view, [], {}))

    @override_settings(BRIDGEKEEPER_COOKIE_NAME='invite_code')
    def test_invalid_invite_code_gorge(self):
        self.request.COOKIES = {'invite_code': 'x'}
        self.assertFalse(valid_invite(self.request, self.view, [], {}))
