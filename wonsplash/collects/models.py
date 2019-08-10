from django.db import models
from taggit.managers import TaggableManager
from wonsplash.users import models as user_model
# Create your models here.
class TimeStamp(models.Model):

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

class Images(TimeStamp):

    file = models.ImageField()
    creator = models.ForeignKey(user_model.User, on_delete=models.CASCADE)
    views = models.IntegerField(null=True, blank=True, default=0)
    tags = TaggableManager()

class Like(TimeStamp):

    image = models.ForeignKey(Images, on_delete=models.CASCADE)
    creator = models.ForeignKey(user_model.User, on_delete=models.CASCADE)