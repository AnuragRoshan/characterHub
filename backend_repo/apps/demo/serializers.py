from rest_framework import serializers
from .models import Post, Comment


class CommentSerializer(serializers.ModelSerializer):
    user_username = serializers.CharField(source='user.username')  # Add username of the user

    class Meta:
        model = Comment
        fields = ['text', 'timestamp', 'user_username']  # Include only required fields


class PostSerializer(serializers.ModelSerializer):
    user_username = serializers.CharField(source='user.username')  # Add username of the user
    comment_count = serializers.SerializerMethodField()  # Count of comments
    comments = serializers.SerializerMethodField()  # Top 3 comments logic

    class Meta:
        model = Post
        fields = ['text', 'timestamp', 'user_username', 'comment_count', 'comments']

    def get_comment_count(self, post):
        """
        Returns the total count of comments for the post.
        """
        return post.comments.count()

    def get_comments(self, post):
        """
        Returns the top 3 latest comments for the post.
        """
        return CommentSerializer(post.comments.order_by('-timestamp')[:3], many=True).data
