from rest_framework import serializers
from taggit_serializer.serializers import TagListSerializerField, TaggitSerializer
from . import models
from wonsplash.users import models as user_model


class UserSumSerializer(serializers.ModelSerializer):

    class Meta:
        model = user_model.User
        fields = [
            "id",
            "username",
            "avatar"
        ]


class ImageSerializer(serializers.ModelSerializer):

    tags = TagListSerializerField()
    creator = UserSumSerializer()

    class Meta:
        model = models.Image
        fields = [
            "id",
            "file",
            "views",
            "natural_time",
            "like_count",
            "creator",
            "tags",
        ]
