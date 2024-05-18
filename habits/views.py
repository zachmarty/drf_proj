from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from habits.models import Habit
from habits.paginations import HabitPaginator
from habits.permissions import IsUserOrSuper
from habits.serializers import HabitSerializer
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework.exceptions import APIException
from rest_framework import status

from habits.validators import check_input_data


# Create your views here.
class HabitViewSet(ModelViewSet):
    serializer_class = HabitSerializer
    queryset = Habit.objects.all()
    http_method_names = ["get", "post", "put", "delete"]
    pagination_class = HabitPaginator

    def get_permissions(self):
        if self.action == "list":
            self.permission_classes = [IsAuthenticated]
        elif self.action == "retrieve":
            self.permission_classes = [IsAuthenticated]
        elif self.action == "create":
            self.permission_classes = [IsAuthenticated]
        elif self.action == "update":
            self.permission_classes = [IsAuthenticated, IsUserOrSuper]
        elif self.action == "destroy":
            self.permission_classes = [IsAuthenticated, IsUserOrSuper]
        return [permission() for permission in self.permission_classes]

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.publicated == True or instance.user == request.user:
            serializer = self.get_serializer(instance)
            return Response(serializer.data)
        else:
            raise APIException("Habit is not pulicated", status.HTTP_406_NOT_ACCEPTABLE)

    def list(self, request, *args, **kwargs):
        self.queryset = Habit.objects.filter(publicated=True)
        serializer = self.get_serializer(self.queryset, many=True)
        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT, data="Success")

    def create(self, request, *args, **kwargs):
        data = request.data
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        data : dict = check_input_data(data)
        related_habit = data['related_habit']
        data.pop('related_habit')
        new_habit = Habit.objects.create(**data)
        new_habit.related_habit = related_habit
        new_habit.user = request.user
        new_habit.save()
        return Response(data=data)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop("partial", False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        data = check_input_data(request.data)
        self.perform_update(serializer)
        return Response(serializer.data)


class SelfHabitsView(ListAPIView):
    serializer_class = HabitSerializer
    queryset = Habit.objects.all()
    permission_classes = [IsAuthenticated]
    pagination_class = HabitPaginator

    def get(self, request, *args, **kwargs):
        queryset = Habit.objects.filter(user=request.user)
        paginated_queryset = self.paginate_queryset(queryset)
        serializer = self.get_serializer(paginated_queryset, many=True)
        return Response(serializer.data)