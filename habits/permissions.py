from rest_framework.permissions import BasePermission


class IsUserOrSuper(BasePermission):
    """Права для редактирования и просмотра привычек (владелец или суперпользователь)"""

    def has_object_permission(self, request, view, obj):
        if request.user.is_staff:
            return True
        return obj.user == request.user
