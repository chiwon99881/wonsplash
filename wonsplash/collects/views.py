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

            def get_key(image):
                return image.created_at

            sorted_images = sorted(images, key=get_key, reverse=True)

            serializer = serializers.ImageSerializer(sorted_images, many=True, context={"request": request})

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
            return Response(data="해당 id의 이미지가 존재하지 않습니다", status=status.HTTP_304_NOT_MODIFIED)

        try:
            exist_like = models.Like.objects.get(creator=user, image=get_image)
            exist_like.delete()
            return Response(data="좋아요가 취소되었습니다", status=status.HTTP_200_OK)
        except models.Like.DoesNotExist:
            return Response(data="좋아요가 반영되어 있지않습니다", status=status.HTTP_404_NOT_FOUND)


class Search(APIView):

    def get(self, request, format=None):

        search_term = request.query_params.get('term', None)

        if search_term is not None:

            split_term = search_term.split(",")

            tag_images = models.Image.objects.filter(tags__name__in=split_term).distinct()

            serializer = serializers.ImageSerializer(tag_images, many=True, context={"request": request})

            return Response(data=serializer.data, status=status.HTTP_200_OK)

        else:
            return Response(data="term을 입력해주세요", status=status.HTTP_400_BAD_REQUEST)


class Post(APIView):

    def post(self, request, format=None):

        user = request.user

        serializer = serializers.PostSerializer(data=request.data)

        if serializer.is_valid():

            serializer.save(creator=user)

            return Response(data=serializer.data, status=status.HTTP_201_CREATED)

        else:
            return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class Detail(APIView):

    def found_image(self, image_id):
        try:
            image = models.Image.objects.get(id=image_id)
            return image
        except models.Image.DoesNotExist:
            return None

    def get(self, request, image_id, format=None):

        get_image = self.found_image(image_id)

        if get_image is None:
            return Response(data="해당 id의 이미지가 없습니다", status=status.HTTP_204_NO_CONTENT)
        else:
            serializer = serializers.ImageSerializer(get_image, context={"request": request})
            get_image.views = get_image.views + 1
            get_image.save()
            return Response(data=serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, image_id, format=None):

        user = request.user
        get_image = self.found_image(image_id)

        if get_image is None:
            return Response(data="해당 id의 이미지가 없습니다", status=status.HTTP_204_NO_CONTENT)
        else:
            image_creator_id = models.Image.objects.get(id=image_id).creator.id
            if image_creator_id != user.id:
                return Response(data="권한이 없습니다", status=status.HTTP_401_UNAUTHORIZED)
            else:
                get_image.delete()
                return Response(data="이미지가 삭제되었습니다", status=status.HTTP_200_OK)
