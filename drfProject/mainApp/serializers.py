from rest_framework import serializers
from .models import Review,ModelParameter

class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model=Review
        fields=['id','title','content','updated_at']

class ModelSerializer(serializers.ModelSerializer):
    class Meta:
        model=ModelParameter
        fields=['id','modelname','parameter','result','csv_file','updated_at']