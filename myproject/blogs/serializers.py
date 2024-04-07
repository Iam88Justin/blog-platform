from rest_framework import serializers
from .models import Post, Comment
from django.contrib.auth import get_user_model

class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = '__all__'


User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password')

    def create(self, validated_data):
        user = User.objects.create_user(validated_data['username'], validated_data['email'], validated_data['password'])
        return user

    def validate(self, attrs):
        # You can add custom validation logic here (e.g., check for unique email)
        return attrs

class CommentSerializer(serializers.ModelSerializer):
    # Consider including the author's username or profile information
    author_username = serializers.ReadOnlyField(source='author.username')

    class Meta:
        model = Comment
        fields = ('id', 'author_username', 'content', 'created_at')