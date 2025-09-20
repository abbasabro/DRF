from rest_framework import serializers
from .models import FileUploader

class FileUploaderSerializer(serializers.ModelSerializer):
    class Meta:
        model = FileUploader
        fields = '__all__'