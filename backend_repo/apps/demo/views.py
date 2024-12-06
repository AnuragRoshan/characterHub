# TODO There's certainly more than one way to do this task, so take your pick.

from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Post
from .serializers import PostSerializer
from .models import Comment
from .serializers import CommentSerializer
from .pagination import CustomPagination  # Import the custom pagination class

class PostListView(APIView):
    """
    API endpoint to fetch posts with pagination for infinite scrolling.
    """

    def get(self, request):
        # Query all posts ordered by timestamp
        posts = Post.objects.prefetch_related('comments').order_by('-timestamp')

        # Apply custom pagination
        paginator = CustomPagination()
        paginated_posts = paginator.paginate_queryset(posts, request)

        # Serialize paginated data
        serializer = PostSerializer(paginated_posts, many=True)

        # Return custom paginated response (results only)
        return paginator.get_paginated_response(serializer.data)


class CommentRangeView(APIView):
    """
    Fetch a range of comments for a specific post.
    Endpoint: /posts/{post_id}/comments/{n}/
    """

    def get(self, request, post_id, n):
        # Convert n to integer
        try:
            n = int(n)
        except ValueError:
            return Response({"error": "Invalid range value"}, status=400)

        # Get the comments for the specific post
        comments = Comment.objects.filter(post_id=post_id).order_by('-timestamp')

        # Calculate the range
        start_index = max(0, n - 3)  # Lower bound
        end_index = n  # Upper bound (exclusive)

        # Get the specific range of comments
        selected_comments = comments[start_index:end_index]

        # Serialize the selected comments
        serializer = CommentSerializer(selected_comments, many=True)

        return Response(serializer.data)