import datetime

from django.test import TestCase, override_settings
from django.db.utils import IntegrityError
from django.utils import timezone

from ..models import Invite


class InviteModelTestCase(TestCase):

    def test_expired_none_default(self):
        invite = Invite.objects.create()
        self.assertIsNone(invite.expired)

    @override_settings(BRIDGEKEEPER_INVITE_EXPIRED_SECONDS=360)
    def test_expired_none_uses_settings(self):
        invite = Invite.objects.create()
        self.assertIsNotNone(invite.expired)

    def test_expired_manually_set(self):
        next_week = timezone.now() + datetime.timedelta(days=7)
        invite = Invite.objects.create(expired=next_week)
        self.assertEqual(invite.expired, next_week)

    @override_settings(BRIDGEKEEPER_INVITE_EXPIRED_SECONDS=360)
    def test_expired_manually_set_ignores_settings(self):
        next_week = timezone.now() + datetime.timedelta(days=7)
        invite = Invite.objects.create(expired=next_week)
        self.assertEqual(invite.expired, next_week)

    def test_code_default_shortuuid(self):
        invite = Invite.objects.create()
        self.assertTrue(len(invite.code) >= 1)

    def test_code_manually_set_create(self):
        CODE = 'camelot'
        invite = Invite.objects.create(code=CODE)
        self.assertEqual(invite.code, CODE)

    def test_code_unique(self):
        CODE = 'camelot'
        Invite.objects.create(code=CODE)
        with self.assertRaises(IntegrityError):
            Invite.objects.create(code=CODE)

    def test_is_valid_never_expires_valid(self):
        invite = Invite.objects.create(expired=None)
        self.assertTrue(invite.is_valid())

    def test_is_valid_future_valid(self):
        now = timezone.now()
        future = now + datetime.timedelta(seconds=1)
        invite = Invite.objects.create(expired=future)
        self.assertTrue(invite.is_valid(now=now))

    def test_is_valid_past_not_valid(self):
        now = timezone.now()
        past = now - datetime.timedelta(seconds=1)
        invite = Invite.objects.create(expired=past)
        self.assertFalse(invite.is_valid(now=now))

    def test_is_valid_exactly_same_not_valid(self):
        now = timezone.now()
        invite = Invite.objects.create(expired=now)
        self.assertFalse(invite.is_valid(now=now))
