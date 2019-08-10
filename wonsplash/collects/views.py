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
