from django.urls import path
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from users.apps import UsersConfig
from users.views import UserCreateAPIView, UserRetrieveAPIView, UserListAPIView

app_name = UsersConfig.name

urlpatterns = [
    path('users/create/', UserCreateAPIView.as_view(), name='users_create'),
    path('users/', UserListAPIView.as_view(), name='users_list'),
    path('users/<int:pk>/', UserRetrieveAPIView.as_view(), name='users_retrieve'),
    path('token/', TokenObtainPairView.as_view(permission_classes=(AllowAny,)), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(permission_classes=(AllowAny,)), name='token_refresh'),
]
