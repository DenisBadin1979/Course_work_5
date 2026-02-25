from rest_framework import permissions


class IsOwnerOrPublicReadOnly(permissions.BasePermission):
    """
    Разрешение:
    - Безопасные методы (GET, HEAD, OPTIONS) доступны всем, если привычка публичная или пользователь — владелец.
    - Для остальных методов требуется, чтобы пользователь был владельцем.
    - Создание (POST) разрешено только аутентифицированным пользователям.
    """

    def has_permission(self, request, view):
        # Для создания требуется аутентификация
        if request.method == "POST":
            return request.user and request.user.is_authenticated
        # Для остальных методов разрешаем на уровне запроса
        return True

    def has_object_permission(self, request, view, obj):
        # Проверка на уровне объекта
        if request.method in permissions.SAFE_METHODS:
            # Чтение доступно, если объект публичный или пользователь — владелец
            return obj.is_public or obj.user == request.user
        # Изменение/удаление только для владельца
        return obj.user == request.user
