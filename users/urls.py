from rest_framework_simplejwt.views import TokenRefreshView, TokenObtainPairView
from django.urls import path

from users.apps import UsersConfig
from users.views import UserCreateView

app_name = UsersConfig.name

urlpatterns = [
    path("token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("create", UserCreateView.as_view(), name="user_create"),
]
