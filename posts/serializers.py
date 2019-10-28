from rest_framework import serializers
from .models import Post, Author

class AuthorSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(source='user.email')
    password = serializers.CharField(write_only=True)
    #token_generated = serializers.CharField(source='user.token_generated', read_only=True)
    class Meta:
        model = Author
        fields = '__all__'
        depth = 1

    def create(self, validated_data):
        author = Author.objects.create_author(
            email=validated_data.pop('user')['email'],
            **validated_data)
        author.save()
        return author

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.save()
        return instance

class PostSerializer(serializers.ModelSerializer):
    author_id = serializers.CharField(required=False, allow_blank=True)
    class Meta:
        model = Post
        fields = '__all__'
        depth = 1

    def create(self, validated_data):
        author_id = validated_data.pop('author_id')
        post = Post.objects.create(**validated_data)
        post.author = Author.objects.get(pk=author_id) 
        post.save()
        return post

    def update(self, instance, validated_data):
        instance.title = validated_data.get('title', instance.title)
        instance.content = validated_data.get('content', instance.last_name)
        instance.save()
        return instance
