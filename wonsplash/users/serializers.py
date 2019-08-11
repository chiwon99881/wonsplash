from rest_framework import serializers
from wonsplash.collects import serializers as collects_serializer
from . import models


class UserProfileSerializer(serializers.ModelSerializer):

    images = collects_serializer.ImageSerializer(many=True, read_only=True)
    post_count = serializers.ReadOnlyField()
    following_count = serializers.ReadOnlyField()
    followers_count = serializers.ReadOnlyField()
    is_following = serializers.SerializerMethodField()
    is_self = serializers.SerializerMethodField()

    class Meta:
        model = models.User
        fields = [
            "id",
            "avatar",
            "first_name",
            "last_name",
            "email",
            "username",
            "images",
            "following_count",
            "followers_count",
            "post_count",
            "is_following",
            "is_self",
        ]

    def get_is_following(self, obj):
        if "request" in self.context:
            request = self.context['request']
            if obj in request.user.following.all():
                return True
        return False

    def get_is_self(self, obj):
        if "request" in self.context:
            request = self.context['request']
            print(obj.username, request.user.username)
            if obj.username == request.user.username:
                return True
        return False


class EditSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.User
        fields = [
            "avatar",
            "first_name",
            "last_name",
            "email",
        ]
