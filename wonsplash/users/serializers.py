from rest_framework import serializers
from wonsplash.collects import serializers as collects_serializer
from . import models


class UserProfileSerializer(serializers.ModelSerializer):

    images = collects_serializer.ImageSerializer(many=True, read_only=True)
    post_count = serializers.ReadOnlyField()
    following_count = serializers.ReadOnlyField()
    followers_count = serializers.ReadOnlyField()
    is_following = serializers.SerializerMethodField()

    class Meta:
        model = models.User
        fields = [
            "id",
            "avatar",
            "username",
            "images",
            "following_count",
            "followers_count",
            "post_count",
            "is_following",
        ]

    def get_is_following(self, obj):
        if "request" in self.context:
            request = self.context['request']
            if obj in request.user.following.all():
                return True
        return False
