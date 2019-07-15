from rest_framework import serializers

from .models import Profile

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        exclude = ('password',)

class ProfileWriteSerializer(serializers.Serializer):
    username = serializers.CharField(min_length=3, max_length=30, allow_blank=False, trim_whitespace=True)
    password = serializers.CharField(required=False)

    def update(self, instance, validated_data):
        instance.username = validated_data.get('username', instance.username)
        if 'password' in validated_data:
            instance.set_password(validated_data.get('password'))
        instance.save()
        return instance