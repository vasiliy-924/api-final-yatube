from typing import Any

from django.shortcuts import get_object_or_404
from rest_framework import filters, viewsets
from rest_framework.mixins import CreateModelMixin, ListModelMixin
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import IsAuthenticated

from api.serializers import (
    CommentSerializer,
    GroupSerializer,
    PostSerializer,
    FollowSerializer
)
from api.permissions import IsAuthorOrReadOnly
from posts.models import Group, Post


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


class FollowViewSet(ListModelMixin, CreateModelMixin, viewsets.GenericViewSet):
    """Представление для модели Follow."""

    serializer_class = FollowSerializer
    permission_classes = (IsAuthenticated,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('following__username',)

    def get_queryset(self) -> Any:
        """
        Получает список подписок текущего пользователя.
        Returns:
            QuerySet: Набор подписок пользователя
        """
        return self.request.user.follower.all()

    def perform_create(self, serializer: FollowSerializer) -> None:
        """
        Создает новую подписку.
        Args:
            serializer: Сериализатор подписки
        """
        serializer.save(user=self.request.user)
