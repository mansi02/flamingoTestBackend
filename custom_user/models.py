from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver

from rest_framework.authtoken.models import Token


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)


class User(AbstractUser):
    username = models.CharField(
        max_length=255,
        unique=True,
        null=False,
    )
    email = models.EmailField(
        max_length=255,
        unique=True,
        null=False,
    )
    profile_image = models.ImageField(
        upload_to='User',
        null=True,
    )

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []

    def __str__(self):
        return '{} : {}'.format(self.pk, self.email)
