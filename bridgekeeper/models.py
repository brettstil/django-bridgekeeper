import uuid
import datetime

from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone
from django.conf import settings
from django.core.validators import validate_slug

import shortuuid


# makemigrations keeps making new migrations with default=shortuuid.uuid
def generate_code():
    short = shortuuid.ShortUUID()
    return short.uuid()


class Invite(models.Model):

    id = models.UUIDField(
        _('id'), primary_key=True, default=uuid.uuid4, editable=False)
    created = models.DateTimeField(
        _('created'), auto_now_add=True, editable=False)
    updated = models.DateTimeField(
        _('updated'), auto_now=True, editable=False)

    code = models.CharField(
        _('code'),
        max_length=255,
        unique=True,
        db_index=True,
        default=generate_code,
        validators=[validate_slug],
    )

    expired = models.DateTimeField(
        _('expired'),
        null=True,
        blank=True,
        help_text=_('Invite not valid after expired datetime'))

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        help_text=_('Invite creator'),
        related_name='invites')

    def __str__(self):
        return self.code

    def save(self, *args, **kwargs):

        INVITE_EXPIRED_SECONDS = getattr(
            settings, 'BRIDGEKEEPER_INVITE_EXPIRED_SECONDS', None)
        if INVITE_EXPIRED_SECONDS and self.created is None and \
                self.expired is None:  # allow manually set expired
            self.expired = timezone.now() + datetime.timedelta(
                seconds=INVITE_EXPIRED_SECONDS)

        super(Invite, self).save(*args, **kwargs)

    def is_valid(self, now=None):
        if now is None:
            now = timezone.now()
        return self.expired is None or self.expired > now
