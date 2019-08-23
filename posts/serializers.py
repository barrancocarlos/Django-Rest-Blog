from rest_framework import serializers
from .models import Post, Author

class AuthorSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(source='user.email')
    password = serializers.CharField(write_only=True)
    #token_generated = serializers.CharField(source='user.token_generated', read_only=True)
    class Meta:
        model = Author
        fields = ('id', 'name', 'last_name', 'email', 'password')

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
    class Meta:
        model = Post
        fields = ('id', 'title', 'content', 'created_at', 'updated_at', 'author')
        depth = 1
