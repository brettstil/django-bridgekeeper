import datetime

from django.test import TestCase, override_settings
from django.urls import reverse
from django.utils import timezone

from ..models import Invite


@override_settings(
    BRIDGEKEEPER_URL_INVITED_OK='/ok/',
    BRIDGEKEEPER_URL_INVITED_INVALID='/invalid/',
    BRIDGEKEEPER_COOKIE_NAME='invite_code',
)
class InvitedViewTestCase(TestCase):
    def setUp(self):
        self.URL_INVITED_OK = '/ok/'
        self.URL_INVITED_INVALID = '/invalid/'
        self.COOKIE_NAME = 'invite_code'

    def test_invite_valid(self):
        invite = Invite.objects.create()
        url = reverse('invited', kwargs={'code': invite.code})
        response = self.client.get(url)
        self.assertIn(self.COOKIE_NAME, response.cookies)
        self.assertEqual(response.cookies[self.COOKIE_NAME].value, invite.code)
        self.assertEqual(response.url, self.URL_INVITED_OK)

    def test_invite_code_does_not_exist_invalid(self):
        url = reverse('invited', kwargs={'code': 'x'})
        response = self.client.get(url)
        self.assertNotIn(self.COOKIE_NAME, response.cookies)
        self.assertEqual(response.url, self.URL_INVITED_INVALID)

    def test_invite_is_valid_false_invalid(self):
        yesterday = timezone.now() - datetime.timedelta(days=1)
        invite = Invite.objects.create(expired=yesterday)
        url = reverse('invited', kwargs={'code': invite.code})
        response = self.client.get(url)
        self.assertNotIn(self.COOKIE_NAME, response.cookies)
        self.assertEqual(response.url, self.URL_INVITED_INVALID)

    @override_settings(USE_TZ=True, TIME_ZONE='UTC')
    def test_invite_expired_none_utc(self):
        invite = Invite.objects.create()
        url = reverse('invited', kwargs={'code': invite.code})
        response = self.client.get(url)
        cookie = response.cookies[self.COOKIE_NAME]
        self.assertEqual(cookie.value, invite.code)
        self.assertEqual('', cookie['expires'])

    @override_settings(USE_TZ=True, TIME_ZONE='UTC')
    def test_invite_expired_aware_utc(self):
        tomorrow = timezone.now() + datetime.timedelta(days=1)
        invite = Invite.objects.create(expired=tomorrow)
        url = reverse('invited', kwargs={'code': invite.code})
        response = self.client.get(url)
        cookie = response.cookies[self.COOKIE_NAME]
        self.assertEqual(cookie.value, invite.code)
        self.assertNotEqual('', cookie['expires'])
