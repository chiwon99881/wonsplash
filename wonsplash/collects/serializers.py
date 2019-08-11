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
    is_liked = serializers.SerializerMethodField()

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
            "is_liked",
        ]

    def get_is_liked(self, obj):
        if "request" in self.context:
            request = self.context['request']
            try:
                models.Like.objects.get(image=obj, creator=request.user)
                return True
            except models.Like.DoesNotExist:
                return False


class PostSerializer(TaggitSerializer, serializers.ModelSerializer):

    tags = TagListSerializerField()

    class Meta:
        model = models.Image
        fields = [
            "id",
            "file",
            "tags",
        ]


class LikeSerializer(serializers.ModelSerializer):

    image = ImageSerializer()

    class Meta:
        model = models.Like
        fields = [
            "id",
            "image",
            "natural_time",
        ]
