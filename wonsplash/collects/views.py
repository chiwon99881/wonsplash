from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from . import models, serializers
# Create your views here.


class Feed(APIView):

    def get(self, request, format=None):

        try:
            images = models.Image.objects.all()

            serializer = serializers.ImageSerializer(images, many=True)

            return Response(data=serializer.data, status=status.HTTP_200_OK)

        except models.Image.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)


class Like(APIView):

    def found_image(self, image_id):
        try:
            image = models.Image.objects.get(id=image_id)
            return image
        except models.Image.DoesNotExist:
            return None

    def post(self, request, image_id, format=None):

        user = request.user

        get_image = self.found_image(image_id)

        if get_image is None:
            return Response(data="해당 id의 이미지가 존재하지 않습니다", status=status.HTTP_404_NOT_FOUND)

        try:
            exist_like = models.Like.objects.get(creator=user, image=get_image)
            return Response(data="이미 좋아요를 누른상태입니다", status=status.HTTP_304_NOT_MODIFIED)
        except models.Like.DoesNotExist:
            create_like = models.Like.objects.create(image=get_image, creator=user)
            create_like.save()

            return Response(data="좋아요가 반영되었습니다", status=status.HTTP_201_CREATED)


class UnLike(APIView):

    def found_image(self, image_id):
        try:
            image = models.Image.objects.get(id=image_id)
            return image
        except models.Image.DoesNotExist:
            return None

    def delete(self, request, image_id, format=None):

        user = request.user

        get_image = self.found_image(image_id)
        if get_image is None:
            return Response(data="해당 id의 이미지가 존재하지 않습니다", status=HTTP_304_NOT_MODIFIED)

        try:
            exist_like = models.Like.objects.get(creator=user, image=get_image)
            exist_like.delete()
            return Response(data="좋아요가 취소되었습니다", status=status.HTTP_200_OK)
        except models.Like.DoesNotExist:
            return Response(data="좋아요가 반영되어 있지않습니다", status=status.HTTP_404_NOT_FOUND)
