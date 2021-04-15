from django.shortcuts import get_object_or_404
from rest_framework import serializers
from .models import *


class CommentSerializer(serializers.ModelSerializer):
    doctor = serializers.CharField(max_length=255)

    class Meta:
        model = Comment
        fields = ['doctor', 'comment_text']

