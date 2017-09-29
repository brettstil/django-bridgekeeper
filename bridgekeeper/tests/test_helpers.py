
from unittest.mock import Mock

from django.test import TestCase, override_settings

from ..helpers import get_invite, get_invite_code
from ..models import Invite


@override_settings(BRIDGEKEEPER_COOKIE_NAME='cookie_name')
class GetInviteRequestTestCase(TestCase):

    def setUp(self):
        self.COOKIE_NAME = 'cookie_name'
        self.CODE = '123'
        self.request = Mock()
        self.request.COOKIES = {}

    def test_get_invite_code_found(self):
        self.request.COOKIES[self.COOKIE_NAME] = self.CODE
        code = get_invite_code(self.request)
        self.assertEqual(code, self.CODE)

    def test_get_invite_code_none(self):
        code = get_invite_code(self.request)
        self.assertEqual(code, None)

    def test_get_invite_found(self):
        created = Invite.objects.create(code=self.CODE)
        self.request.COOKIES[self.COOKIE_NAME] = created.code
        invite = get_invite(self.request)
        self.assertEqual(invite, created)

    def test_get_invite_none(self):
        invite = get_invite(self.request)
        self.assertIsNone(invite)
