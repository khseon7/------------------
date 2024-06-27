import os
from django.conf import settings
from django.shortcuts import render
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import Http404

from .serializers import ReviewSerializer,ModelSerializer
from .models import Review,ModelParameter

# Create your views here.
class ReviewList(APIView):
    def get(self, request):
        reviews=Review.objects.all()
        serializer=ReviewSerializer(reviews, many=True)
        return Response(serializer.data)
    def post(self, request):
        serializer=ReviewSerializer(
            data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

class ReviewDetail(APIView):
    def get_object(self, pk):
        try:
            return Review.objects.get(pk=pk)
        except Review.DoesNotExist:
            raise Http404
    def get(self, request, pk, format=None):
        review=self.get_object(pk)
        serializer=ReviewSerializer(review)
        return Response(serializer.data)
    def put(self, request, pk, format=None):
        review=self.get_object(pk)
        serializer=ReviewSerializer(review,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    def delete(self, request, pk, format=None):
        review=self.get_object(pk)
        review.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class ModelList(APIView):
    def get(self, request):
        reviews=ModelParameter.objects.all()
        serializer=ModelSerializer(reviews, many=True)
        return Response(serializer.data)
    def post(self, request):
        serializer=ModelSerializer(
            data=request.data)
        if serializer.is_valid():
            if 'csv_file' in request.FILES:
                serializer.validated_data['csv_file'] = request.FILES['csv_file']
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

class ModelDetail(APIView):
    def get_object(self, pk):
        try:
            return ModelParameter.objects.get(pk=pk)
        except ModelParameter.DoesNotExist:
            raise Http404
    def get(self, request, pk, format=None):
        model=self.get_object(pk)
        serializer=ModelSerializer(model)
        return Response(serializer.data)
    def put(self, request, pk, format=None):
        model=self.get_object(pk)
        serializer=ModelSerializer(model,data=request.data)
        if serializer.is_valid():
            if 'csv_file' in request.FILES:
                serializer.validated_data['csv_file'] = request.FILES['csv_file']
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    def delete(self, request, pk, format=None):
        model = self.get_object(pk)
        if model.csv_file:
            csv_file_path = os.path.join(settings.MEDIA_ROOT, model.csv_file.name)
            if os.path.exists(csv_file_path):
                os.remove(csv_file_path)
        model.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)