from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser
from django.db import models
from foodgram.validators import validate_username


class Profile(AbstractUser):
    email = models.EmailField(max_length=254, unique=True)
    first_name = models.CharField(max_length=150)
    username = models.CharField(
        max_length=150, unique=True,
        validators=(validate_username,)
    )
    last_name = models.CharField(max_length=150)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'username', 'last_name',]

    class Meta:
        verbose_name = 'пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self) -> str:
        return f'{self.email} ({self.username})'


User = get_user_model()


class Follow(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='subscriptions',
        verbose_name='Пользователь'
    )
    following = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='users',
        verbose_name='На кого подписан'
    )

    class Meta:
        verbose_name = 'подписки'
        verbose_name_plural = 'Подписки'
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'following'],
                name='unique_subscriptions'
            ),
        ]

    def __str__(self):
        return ('{} подписан на рецепты {}'.format(self.user, self.following))
