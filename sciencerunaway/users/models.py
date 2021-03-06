# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import

from django.contrib.auth.models import AbstractUser
from django.contrib.postgres.fields import JSONField
from django.core.urlresolvers import reverse
from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User


@python_2_unicode_compatible
class User(AbstractUser):

    # First Name and Last Name do not cover name patterns
    # around the globe.
    name = models.CharField(_('Name of User'), blank=True, max_length=255)

    def __str__(self):
        return self.username

    def get_absolute_url(self):
        return reverse('users:detail', kwargs={'username': self.username})


class UserProfile(models.Model):
    choice_dropdown = [(1, 'Girls'), (2, 'Role Model')]
    name = models.TextField(null=True, blank=True)
    linkedin = models.TextField(null=True, blank=True)
    bio = models.TextField(null=True, blank=True)
    user = models.OneToOneField(User, related_name='profile')
    # image = models.ImageField(
    #     upload_to='userpics/', null=True, blank=True
    # )
    image = models.TextField(
        null=True, blank=True
    )
    age = models.IntegerField(default=0)
    signup_type = models.IntegerField(
        _('User Type'),
        choices=choice_dropdown,
        default=1
    )
    has_quiz_attempted = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)
    common_answers = JSONField(null=True, blank=True)
    other_answers = JSONField(null=True, blank=True)

    def __unicode__(self):
        return self.user.username

    def user_active(self):
        return self.user.is_active

    class Meta:
        db_table = 'user_profile'


class Mentors(models.Model):
    """Mentor class."""
    girl = models.ForeignKey(
        UserProfile,
        null=True,
        blank=True,
        related_name="girl"
    )

    mentor = models.ForeignKey(
        UserProfile,
        null=True,
        blank=True,
        related_name="mentor"
    )
