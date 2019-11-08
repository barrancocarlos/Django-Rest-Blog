from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from django.http import Http404, HttpResponse
from django.db import IntegrityError

from rest_framework import status, viewsets
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
        #get author by user id
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


class PostViewset(viewsets.ViewSet):
    permission_classes = (IsAuthenticatedOrReadOnly,)
    def get_object(self, pk):
        try:
            return Post.objects.get(pk=pk)
        except Post.DoesNotExist:
            raise Http404

    def list(self, request):
        posts = Post.objects.all()    
        #get post by author
        author_id = self.request.query_params.get('author_id', None)
        if author_id is not None:
            posts = posts.filter(author_id=author_id)
        serializer = PostSerializer(posts, many=True, context={"request": request})
        return Response(serializer.data)
    
    def retrieve(self, request, pk=None):
        post = self.get_object(pk)
        serializer = PostSerializer(post, context={"request": request})
        return Response(serializer.data)

    def create(self, request):        
        serializer = PostSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)            
        the_response = PostSerializer(serializer.save())
        return Response(the_response.data, status=status.HTTP_201_CREATED)       

    def update(self, request, pk=None):
        post = self.get_object(pk)
        serializer = PostSerializer(post, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        post = self.get_object(pk)
        post.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
