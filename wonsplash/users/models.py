from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _


class User(AbstractUser):
    """ User Model """
    # First Name and Last Name do not cover name patterns
    # around the globe.
    avatar = models.CharField(max_length=1000, null=True, blank=True, default="")
    followers = models.ManyToManyField("self", blank=True, symmetrical=False, related_name="followers_set")
    following = models.ManyToManyField("self", blank=True, symmetrical=False, related_name="following_set")

    def post_count(self):
        return self.images.all().count()

    def following_count(self):
        return self.following.all().count()

    def followers_count(self):
        return self.followers.all().count()
