from rest_framework.permissions import SAFE_METHODS, BasePermission


class CustomBasePermission(BasePermission):
    """Базовый класс разрешений."""

    def has_permission(self, request, view):
        return (
            request.method in SAFE_METHODS
            or request.user.id is not None
            and request.user.is_authenticated
            and request.user.is_active
        )


class AuthorStaffOrReadOnly(CustomBasePermission):
    """
    Разрешение на изменение только для служебного персонала и автора.
    Остальным только чтение объекта.
    """

    def has_object_permission(self, request, view, obj):
        return (
            request.method in SAFE_METHODS
            or request.user.id is not None
            and request.user.is_authenticated
            and request.user.is_active
            and (request.user == obj.author or request.user.is_staff)
        )
