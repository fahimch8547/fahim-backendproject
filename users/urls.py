from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from .views import register_user, login_user, UserProfileView

urlpatterns = [
    path('register/', register_user, name='register'),
    path('login/', login_user, name='login'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('profile/', UserProfileView.as_view(), name='profile'),
]