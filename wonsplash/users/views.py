from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from . import serializers, models


class Profile(APIView):

    def get_user(self, username):

        try:
            found_user = models.User.objects.get(username=username)
            return found_user
        except models.User.DoesNotExist:
            return None

    def get(self, request, username, format=None):

        found_user = self.get_user(username)

        if found_user is None:

            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = serializers.UserProfileSerializer(found_user, context={"request": request})

        return Response(data=serializer.data, status=status.HTTP_200_OK)
