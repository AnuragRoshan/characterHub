from django.urls import path, include
from rest_framework import routers
from django.http import JsonResponse
from apps.demo.views import PostListView

from apps.demo.views import CommentRangeView

# Health check view
def health_check(request):
    return JsonResponse({"status": "ok", "message": "API is running"})

# Default Router
router = routers.DefaultRouter()

# URL patterns
urlpatterns = [
    path('', include(router.urls)),
    path('health/', health_check, name='health-check'),  # Health check endpoint
    path('posts/', PostListView.as_view(), name='post-list'),  # Add the posts endpoint
    path('posts/<uuid:post_id>/comments/<int:n>/', CommentRangeView.as_view(), name='comment-range'),
]
