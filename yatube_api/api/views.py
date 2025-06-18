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


class FollowViewSet(viewsets.ViewSet):
    """Представление для модели Follow."""

    serializer_class = FollowSerializer
    permission_classes = (IsAuthenticated,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('following__username',)

    def list(self, request: Request) -> Response:
        """
        Возвращает список подписок текущего пользователя.

        Args:
            request: Запрос

        Returns:
            Response: Список подписок
        """
        queryset = request.user.follower.all()
        if request.query_params.get('search'):
            queryset = queryset.filter(
                following__username__icontains=request.query_params['search']
            )
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data)

    def create(self, request: Request) -> Response:
        """
        Создает новую подписку.

        Args:
            request: Запрос

        Returns:
            Response: Созданная подписка
        """
        serializer = self.serializer_class(
            data=request.data,
            context={'request': request}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save(user=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
