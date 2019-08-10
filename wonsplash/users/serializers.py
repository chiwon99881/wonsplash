from rest_framework import serializers
from wonsplash.collects import serializers as collects_serializer
from . import models


class UserProfileSerializer(serializers.ModelSerializer):

    images = collects_serializer.ImageSerializer(many=True, read_only=True)
    is_following = serializers.SerializerMethodField()

    class Meta:
        model = models.User
        fields = [
            "id",
            "avatar",
            "username",
            "images",
            "followers_set",
            "following_set",
            "is_following",
        ]

    def get_is_following(self, obj):
        if "request" in self.context:
            request = self.context['request']
            if obj in request.user.following.all():
                return True
        return False
