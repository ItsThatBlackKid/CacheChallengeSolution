from rest_framework import serializers
from .models import Document


# This class helps convert Model objects into dicts and vice versa
class DocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Document
        fields = ('id', 'message',)
        read_only_fields = ('id',)
