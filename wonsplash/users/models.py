from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _


class User(AbstractUser):
    """ User Model """
    # First Name and Last Name do not cover name patterns
    # around the globe.
    avatar = models.ImageField(null=True ,blank=True)
    followers = models.ManyToManyField("self", blank=True, symmetrical=False, related_name="followers_set")
    following = models.ManyToManyField("self", blank=True, symmetrical=False, related_name="following_set")

    def get_absolute_url(self):
        return reverse("users:detail", kwargs={"username": self.username})
