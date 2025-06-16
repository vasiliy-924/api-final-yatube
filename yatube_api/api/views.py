from typing import Any

from django.shortcuts import get_object_or_404
from rest_framework import filters, status, viewsets
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response

from api.serializers import (
    CommentSerializer,
    GroupSerializer,
    PostSerializer,
    FollowSerializer
)
from api.permissions import IsAuthorOrReadOnly
from posts.models import Group, Post, Follow


class CommentViewSet(viewsets.ModelViewSet):
    """Представление для модели Comment."""
    serializer_class = CommentSerializer
    permission_classes = (IsAuthorOrReadOnly,)

    def get_post(self) -> Post:
        """
        Получает пост для комментария.
        Returns:
            Post: Экземпляр поста
        Raises:
            Http404: Если пост не найден
        """
        return get_object_or_404(Post, pk=self.kwargs.get('post_id'))

    def get_queryset(self) -> Any:
        """
        Получает список комментариев для поста.
        Returns:
            QuerySet: Набор комментариев
        """
        return self.get_post().comments.all()

    def perform_create(self, serializer: CommentSerializer) -> None:
        """
        Создает новый комментарий.

        Args:
            serializer: Сериализатор комментария
        """
        serializer.save(
            author=self.request.user,
            post=self.get_post()
        )


class GroupViewSet(viewsets.ReadOnlyModelViewSet):
    """Представление для модели Group."""
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = (IsAuthorOrReadOnly,)


class PostViewSet(viewsets.ModelViewSet):
    """Представление для модели Post."""
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    pagination_class = LimitOffsetPagination
    permission_classes = (IsAuthorOrReadOnly,)

    def perform_create(self, serializer: PostSerializer) -> None:
        """
        Создает новый пост.
        Args:
            serializer: Сериализатор поста
        """
        serializer.save(author=self.request.user)


class FollowViewSet(viewsets.ModelViewSet):
    """Представление для модели Follow."""
    queryset = Follow.objects.none()
    serializer_class = FollowSerializer
    permission_classes = (IsAuthenticated,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('following__username',)
    http_method_names = ['get', 'post']

    def get_queryset(self) -> Any:
        """
        Получает список подписок текущего пользователя.
        Returns:
            QuerySet: Набор подписок
        """
        return Follow.objects.filter(user=self.request.user)

    def perform_create(self, serializer: FollowSerializer) -> None:
        """
        Создает новую подписку.
        Args:
            serializer: Сериализатор подписки
        """
        serializer.save(user=self.request.user)

    def retrieve(self, request: Request, *args: Any, **kwargs: Any):
        """
        Переопределяет метод retrieve для возврата 404 для объектов подписки.
        Args:
            request: Объект запроса
        Returns:
            Response: Ответ с кодом 404
        """
        return Response(status=status.HTTP_404_NOT_FOUND)

    def create(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        """
        Создает новую подписку.
        Args:
            request: Объект запроса
        Returns:
            Response: Данные созданной подписки
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED,
            headers=headers
        )
