from rest_framework import permissions


class IsAuthorOrReadOnly(permissions.BasePermission):
    """
    Только авторы объекта могут редактировать его.
    Разрешения на чтение разрешены для любого запроса.
    """

    def has_permission(self, request, view) -> bool:
        """
        Проверяет, имеет ли запрос разрешение на доступ к представлению.
        Args:
            request: Объект запроса
            view: Представление, к которому осуществляется доступ
        Returns:
            bool: True, если запрос безопасный или пользователь с токеном
        """
        return (
            request.method in permissions.SAFE_METHODS
            or request.user.is_authenticated
        )

    def has_object_permission(self, request, view, obj) -> bool:
        """
        Проверяет, имеет ли запрос разрешение на доступ к конкретному объекту.
        Args:
            request: Объект запроса
            view: Представление, к которому осуществляется доступ
            obj: Объект, к которому осуществляется доступ
        Returns:
            bool: True, если запрос безопасный или пользователь автор
        """
        return (
            request.method in permissions.SAFE_METHODS
            or obj.author == request.user
        )
