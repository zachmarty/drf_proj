from django.shortcuts import render

# Create your views here.
from rest_framework.generics import CreateAPIView
from django.contrib.auth.hashers import make_password
from users.models import User
from users.serializers import UserSerializer


class UserCreateView(CreateAPIView):
    """Апи создания пользователя"""

    serializer_class = UserSerializer
    queryset = User.objects.all()

    def perform_create(self, serializer):
        new_user = serializer.save()
        new_user.password = make_password(new_user.password)
        new_user.save()
