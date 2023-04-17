import string
import uuid
from datetime import timedelta

from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from django.dispatch import receiver
from django.db import models
import random


class CustomUser(AbstractUser):
    class Meta:
        verbose_name = _('User')
        verbose_name_plural = _('Users')


class Profile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    birth_date = models.DateTimeField(null=True)

    @receiver(post_save, sender=CustomUser)
    def create_profile(sender, instance, created, **kwargs):
        if created:
            Profile.objects.create(user=instance)


class OtpRequest(models.Model):
    class OtpChannel(models.TextChoices):
        ANDROID = _('Android')
        IOS = _('ios')
        WEB = _('Web')

    request_id = models.UUIDField(default=uuid.uuid4, editable=False)
    channel = models.CharField(_('channel'), choices=OtpChannel.choices, max_length=12)
    phone = models.CharField(max_length=12)
    password = models.CharField(max_length=4, null=True)
    valid_from = models.DateTimeField(default=timezone.now)
    valid_until = models.DateTimeField(default=timezone.now() + timedelta(hours=12000))
    receipt_id = models.CharField(max_length=255, null=True)

    def generate_password(self):
        self.password = self._random_password()
        self.valid_until = timezone.now() + timedelta(hours=12000)

    def _random_password(self):
        rand = random.SystemRandom()
        digits = rand.choices(string.digits, k=4)
        return ''.join(digits)

    class Meta:
        verbose_name = _('One Time Password')
        verbose_name_plural = _('One Time Passwords')