from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from . import serializers, models
from wonsplash.collects import models as collects_model
from wonsplash.collects import serializers as collects_serializer
from allauth.socialaccount.providers.facebook.views import FacebookOAuth2Adapter
from rest_auth.registration.views import SocialLoginView


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

    def put(self, request, username, format=None):

        user = request.user
        will_edit_user = self.get_user(username)

        if will_edit_user is None:
            return Response(data="해당 닉네임의 유저가 없습니다", status=status.HTTP_404_NOT_FOUND)
        else:
            if will_edit_user.username == user.username:
                serializer = serializers.EditSerializer(will_edit_user, data=request.data, partial=True)

                if serializer.is_valid():

                    serializer.save()
                    return Response(data=serializer.data, status=status.HTTP_200_OK)

                else:
                    return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response(data="권한이 없습니다", status=status.HTTP_401_UNAUTHORIZED)


class MyLikes(APIView):

    def get(self, request, format=None):

        user = request.user

        try:
            mylikes = models.User.objects.get(id=user.id).likes.all().order_by('-created_at')

            serializer = collects_serializer.LikeSerializer(mylikes, many=True)

            return Response(data=serializer.data, status=status.HTTP_200_OK)
        except models.User.DoesNotExist:

            return Response(data="request에 user가 없습니다", status=status.HTTP_400_BAD_REQUEST)


class Following(APIView):

    def found_user(self, user_id):

        try:
            user = models.User.objects.get(id=user_id)
            return user
        except models.User.DoesNotExist:
            return None

    def post(self, request, user_id, format=None):
        user = request.user
        get_user = self.found_user(user_id)

        if get_user is None:
            return Response(data="해당 id의 유저가 존재하지 않습니다", status=status.HTTP_204_NO_CONTENT)
        else:
            try:
                already = models.User.objects.get(id=user.id, following__id=get_user.id)
                return Response(data="이미 팔로우중", status=status.HTTP_304_NOT_MODIFIED)
            except models.User.DoesNotExist:
                user.following.add(get_user)
                get_user.followers.add(user)

                user.save()
                get_user.save()

                return Response(data="팔로잉 성공", status=status.HTTP_200_OK)


class UnFollowing(APIView):

    def found_user(self, user_id):
        try:
            user = models.User.objects.get(id=user_id)
            return user
        except models.User.DoesNotExist:
            return None

    def post(self, request, user_id, format=None):

        user = request.user
        get_user = self.found_user(user_id)

        if get_user is None:
            return Response(data="해당 id의 유저가 존재하지 않습니다", status=status.HTTP_204_NO_CONTENT)

        try:
            already = models.User.objects.get(id=user.id, following__id=get_user.id)
            user.following.remove(get_user)
            get_user.followers.remove(user)

            user.save()
            get_user.save()
            return Response(data="언팔 성공", status=status.HTTP_200_OK)
        except models.User.DoesNotExist:
            return Response(data="팔로우중이지 않습니다", status=status.HTTP_400_BAD_REQUEST)


class FacebookLogin(SocialLoginView):
    adapter_class = FacebookOAuth2Adapter
