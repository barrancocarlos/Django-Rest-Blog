from django.shortcuts import render
from rest_framework import viewsets

from django.http import Http404, HttpResponse
from django.db import IntegrityError

from rest_framework import status, viewsets
from rest_framework.decorators import detail_route, list_route
from rest_framework.response import Response

from .models import Author, Post
from .serializers import AuthorSerializer, PostSerializer 
from authentication import utils
from . import models
from . import serializers


# Create your views here.

class AuthorViewset(viewsets.ViewSet):
    def get_object(self, pk):
        try:
            return Author.objects.get(pk=pk)
        except Author.DoesNotExist:
            raise Http404
    
    def list(self, request):
        authors = Author.objects.all()
        user_id = self.request.query_params.get('user_id', None)
        if user_id is not None:
            authors = authors.filter(user=user_id)
        serializer = AuthorSerializer(authors, many=True, context={"request": request})
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        author = self.get_object(pk)
        serializer = AuthorSerializer(author, context={"request": request})
        return Response(serializer.data)

    def create(self, request):
        try:
            serializer = AuthorSerializer(data=request.data)
            if serializer.is_valid():
                the_response = AuthorSerializer(serializer.save())
                return Response(the_response.data, status=status.HTTP_201_CREATED)
        except IntegrityError as e:
            print(e)
            return Response({"message": "Email already in use."}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk=None):
        author = self.get_object(pk)
        serializer = AuthorSerializer(author, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        author = self.get_object(pk)
        author.user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    # @detail_route(methods=['post'], url_path='generate-token')
    # def generate_pwd_token(self, request, pk=None):
    #     exec_admin = self.get_object(pk)
    #     pwd = utils.generate_password()
    #     exec_admin.user.set_password(pwd)
    #     exec_admin.user.token_generated = pwd
    #     exec_admin.user.save()
    #     return Response(pwd, status=status.HTTP_200_OK)


class PostViewset(viewsets.ModelViewSet):
    queryset = models.Post.objects.all()
    serializer_class = serializers.PostSerializer
