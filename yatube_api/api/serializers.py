from typing import Any, Dict

from django.contrib.auth import get_user_model
from rest_framework import serializers

from posts.models import Group, Post, Comment, Follow


User = get_user_model()


class GroupSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Group."""

    class Meta:
        model = Group
        fields = '__all__'


class PostSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Post."""

    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True
    )

    class Meta:
        model = Post
        fields = '__all__'


class CommentSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Comment."""

    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username'
    )

    class Meta:
        model = Comment
        fields = '__all__'
        read_only_fields = ('post',)


class FollowSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Follow."""

    user = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username'
    )
    following = serializers.SlugRelatedField(
        queryset=User.objects.all(),
        slug_field='username'
    )

    class Meta:
        model = Follow
        fields = ('user', 'following')

    def validate(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Проверяет данные подписки.

        Args:
            data: Данные для проверки

        Returns:
            Dict[str, Any]: Проверенные данные

        Raises:
            serializers.ValidationError: Если проверка не пройдена
        """
        user = self.context['request'].user
        following = data['following']

        if user == following:
            raise serializers.ValidationError(
                'Нельзя подписаться на самого себя'
            )

        if Follow.objects.filter(
            user=user,
            following=following
        ).exists():
            raise serializers.ValidationError(
                'Вы уже подписаны на этого пользователя'
            )

        return data

    def to_internal_value(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Удаляет поле user из данных запроса.

        Args:
            data: Данные для обработки

        Returns:
            Dict[str, Any]: Обработанные данные
        """
        if isinstance(data, dict) and 'user' in data:
            data = data.copy()
            data.pop('user')
        return super().to_internal_value(data)

    def create(self, validated_data: Dict[str, Any]) -> Follow:
        """
        Создает новый экземпляр подписки.

        Args:
            validated_data: Проверенные данные

        Returns:
            Follow: Созданный экземпляр подписки
        """
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)
