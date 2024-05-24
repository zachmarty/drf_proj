import datetime
from pytz import timezone
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from habits.models import Habit
from habits.paginations import HabitPaginator
from habits.permissions import IsUserOrSuper
from habits.serializers import HabitSerializer
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework.exceptions import APIException, NotFound
from rest_framework import status
from habits.validators import check_input_data, run_time_validator

class HabitViewSet(ModelViewSet):
    """Вью сет для работы с привычками"""
    serializer_class = HabitSerializer
    queryset = Habit.objects.all()
    http_method_names = ["get", "post", "put", "delete"]
    pagination_class = HabitPaginator

    def get_permissions(self):
        """Получение прав доступа"""
        if self.action == "update" or self.action == "destroy":
            self.permission_classes = [IsAuthenticated, IsUserOrSuper]
        return [permission() for permission in self.permission_classes]

    def retrieve(self, request, *args, **kwargs):
        """Просмотр привычки, если не опубликована - отказ"""
        instance = Habit.objects.filter(id=kwargs["pk"])
        if instance.exists():
            instance = instance.first()
            if instance.publicated == True or instance.user == request.user:
                serializer = self.get_serializer(instance)
                return Response(serializer.data)
            else:
                raise APIException(
                    "Habit is not pulicated", status.HTTP_406_NOT_ACCEPTABLE
                )
        else:
            raise NotFound

    def get_queryset(self):
        """Получение опубликованных привычек + пагинация"""
        queryset = Habit.objects.filter(publicated=True)
        paginated_queryset = self.paginate_queryset(queryset)
        return paginated_queryset

    def destroy(self, request, *args, **kwargs):
        """Немного измененное удаление привычки"""
        instance = Habit.objects.filter(id=kwargs["pk"])
        if not (instance.exists()):
            raise NotFound
        instance = instance.first()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT, data="Success")

    def create(self, request, *args, **kwargs):
        """Создание привычки + проерки + добавление текущего пользователя, последнего запуска, последнего обновления"""
        data = request.data
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        data: dict = check_input_data(data)
        related_habit = data["related_habit"]
        data.pop("related_habit")
        new_habit = Habit.objects.create(**data)
        new_habit.related_habit = related_habit
        new_habit.user = request.user
        if new_habit.usefull == True:
            new_habit.last_run = datetime.date.today()
        new_habit.last_update = datetime.datetime.now(timezone("Europe/Moscow"))
        new_habit.save()
        return Response(data=data)

    def update(self, request, *args, **kwargs):
        """Обновление привычки + проверки"""
        partial = kwargs.pop("partial", False)
        instance = Habit.objects.filter(id=kwargs["pk"])
        if not (instance.exists()):
            raise NotFound
        instance = instance.first()
        data = request.data
        data["last_update"] = datetime.datetime.now(timezone("Europe/Moscow"))
        instance.last_update = datetime.datetime.now(timezone("Europe/Moscow"))
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        data = check_input_data(request.data)
        self.perform_update(serializer)
        run_time_validator(instance)
        return Response(serializer.data)

class SelfHabitsView(ListAPIView):
    """Апи для отображения своих привычек"""
    serializer_class = HabitSerializer
    queryset = Habit.objects.all()
    permission_classes = [IsAuthenticated]
    pagination_class = HabitPaginator

    def get_queryset(self):
        """Получение списка привычек"""
        queryset = Habit.objects.filter(user=self.request.user)
        paginated_queryset = self.paginate_queryset(queryset)
        return paginated_queryset
