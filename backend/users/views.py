from api.serializers import FollowSerializer, ProfileSerializer
from django.contrib.auth import get_user_model
from django.db import IntegrityError
from django.shortcuts import get_object_or_404
from djoser.views import UserViewSet
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from users.models import Follow

User = get_user_model()


class ProfileViewSet(UserViewSet):
    http_method_names = ['get', 'post', 'delete']
    pagination_class = LimitOffsetPagination
    serializer_class = ProfileSerializer

    def get_permissions(self):
        if self.action == 'me':
            return (IsAuthenticated(),)
        return (AllowAny(),)

    def get_queryset(self):
        return User.objects.all()

    @action(
        detail=False,
        methods=['get'],
        permission_classes=[IsAuthenticated],
    )
    def subscriptions(self, request):
        user = request.user
        followings = Follow.objects.filter(user=user)
        queryset = User.objects.filter(
            id__in=followings.values_list('following')
        )
        pages = self.paginate_queryset(queryset)
        serializer = FollowSerializer(
            pages,
            many=True,
            context={'request': request}
        )
        return self.get_paginated_response(serializer.data)

    @action(
        detail=True,
        methods=['post', 'delete'],
        permission_classes=[IsAuthenticated],
    )
    def subscribe(self, request, id):
        if not request.user.id:
            return Response(
                {'errors': 'Запрос от анонимного пользователя!'},
                status=status.HTTP_401_UNAUTHORIZED
            )

        follow = get_object_or_404(User, id=id)
        if request.method == 'POST':
            if request.user.id == int(id):
                raise ValidationError('Попытка подписаться на самого себя!')

            follow = Follow.objects.all().filter(
                following=id
            ).filter(user=request.user)
            if follow.exists():
                raise ValidationError('Подписка уже оформлена!')
            try:
                follow, create = Follow.objects.get_or_create(
                    user=request.user,
                    following=User.objects.get(id=id),
                )
            except IntegrityError:
                raise ValidationError('Что-то навернулось!')
            serializer = FollowSerializer(
                follow.following, context={"request": request}
            )
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        # проверить существует ли запрашиваемый автор
        # follow = get_object_or_404(User, id=id)
        following = Follow.objects.filter(user=request.user, following=follow)
        if not following.exists():
            return Response(
                {'errors': 'Запрашиваемой подписки не сущестовало!'},
                status=status.HTTP_400_BAD_REQUEST
            )
        following.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
