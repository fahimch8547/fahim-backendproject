from django.urls import path
from .views import PostListCreateView, PostDetailView, CommentCreateView, toggle_like

urlpatterns = [
    path('posts/', PostListCreateView.as_view(), name='post-list'),
    path('posts/<int:pk>/', PostDetailView.as_view(), name='post-detail'),
    path('posts/<int:post_id>/comments/', CommentCreateView.as_view(), name='comment-create'),
    path('posts/<int:post_id>/like/', toggle_like, name='toggle-like'),
]