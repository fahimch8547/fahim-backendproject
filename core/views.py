from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse

@api_view(['GET'])
def api_root(request, format=None):
    return Response({
        'message': 'Welcome to Campus Creatives API!',
        'endpoints': {
            'auth': {
                'register': reverse('register', request=request, format=format),
                'login': reverse('login', request=request, format=format),
                'profile': reverse('profile', request=request, format=format),
            },
            'posts': {
                'list_create': reverse('post-list', request=request, format=format),
            },
            'admin': reverse('admin:index', request=request, format=format),
        }
    })