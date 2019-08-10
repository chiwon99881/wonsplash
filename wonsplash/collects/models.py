from django.db import models
from taggit.managers import TaggableManager
from wonsplash.users import models as user_model
from django.contrib.humanize.templatetags.humanize import naturaltime
# Create your models here.


class TimeStamp(models.Model):

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Image(TimeStamp):

    file = models.ImageField()
    creator = models.ForeignKey(user_model.User, on_delete=models.CASCADE, related_name="images")
    views = models.IntegerField(null=True, blank=True, default=0)
    tags = TaggableManager()

    @property
    def natural_time(self):
        return naturaltime(self.created_at)

    @property
    def like_count(self):
        return self.likes.all().count()

    class Meta:
        ordering = ["-created_at"]


class Like(TimeStamp):

    image = models.ForeignKey(Image, on_delete=models.CASCADE, related_name="likes")
    creator = models.ForeignKey(user_model.User, on_delete=models.CASCADE, related_name="likes")
