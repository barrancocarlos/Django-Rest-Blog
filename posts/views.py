from django.shortcuts import render
from django.shortcuts import render
from rest_framework import viewsets
from . import models
from . import serializers

# Create your views here.

class AuthorViewset(viewsets.ModelViewSet):
    queryset = models.Author.objects.all()
    serializer_class = serializers.AuthorSerializer

class PostViewset(viewsets.ModelViewSet):
    queryset = models.Post.objects.all()
    serializer_class = serializers.PostSerializer
