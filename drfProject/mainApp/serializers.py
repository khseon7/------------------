from rest_framework import serializers
from .models import ModelTarget

class ModelSerializer(serializers.ModelSerializer):
    class Meta:
        model=ModelTarget
        fields=['id','modelname','target','result','csv_file','original_filename']