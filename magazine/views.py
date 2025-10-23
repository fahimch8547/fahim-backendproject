from rest_framework import generics, permissions, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django.db.models import Q
from .models import Post, Comment, Like
from .serializers import PostSerializer, PostCreateSerializer, CommentSerializer

class PostListCreateView(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return PostCreateSerializer
        return PostSerializer
    
    def get_queryset(self):
        queryset = Post.objects.all()
        search = self.request.query_params.get('search', None)
        tags = self.request.query_params.get('tags', None)
        
        if search:
            queryset = queryset.filter(
                Q(title__icontains=search) | 
                Q(content__icontains=search) |
                Q(tags__icontains=search)
            )
        
        if tags:
            tag_list = [tag.strip() for tag in tags.split(',')]
            for tag in tag_list:
                queryset = queryset.filter(tags__icontains=tag)
        
        return queryset
    
    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

class PostDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class CommentCreateView(generics.CreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def perform_create(self, serializer):
        post_id = self.kwargs['post_id']
        post = Post.objects.get(id=post_id)
        serializer.save(author=self.request.user, post=post)

@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def toggle_like(request, post_id):
    try:
        post = Post.objects.get(id=post_id)
        like, created = Like.objects.get_or_create(post=post, user=request.user)
        
        if not created:
            like.delete()
            return Response({'liked': False}, status=status.HTTP_200_OK)
        
        return Response({'liked': True}, status=status.HTTP_201_CREATED)
    
    except Post.DoesNotExist:
        return Response({'error': 'Post not found'}, status=status.HTTP_404_NOT_FOUND)