from api.serializers import FollowSerializer, ProfileSerializer
from django.contrib.auth import get_user_model
from django.db import IntegrityError
from django.shortcuts import get_object_or_404
from djoser.views import UserViewSet
from rest_framework import status, viewsets
from rest_framework.decorators import action, api_view
from rest_framework.decorators import permission_classes as permission
from rest_framework.exceptions import ValidationError
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from users.models import Follow

User = get_user_model()


@api_view(['POST', 'DELETE'])
@permission([IsAuthenticated])
def create_subscribe(request, user_id):
    # проверки надо перенести в валидаторс точка пай
    if request.method == 'POST':
        follow = get_object_or_404(User, id=user_id)
        if request.user.id == int(user_id):
            raise ValidationError('Попытка подписаться на самого себя!')

        follow = Follow.objects.all().filter(
            following=user_id
        ).filter(user=request.user)
        if follow.exists():
            raise ValidationError('Подписка уже оформлена!')
        try:
            follow, create = Follow.objects.get_or_create(
                user=request.user,
                following=User.objects.get(id=user_id),
            )
        except IntegrityError:
            raise ValidationError('Что-то навернулось!')
        serializer = FollowSerializer(
            follow.following, context={"request": request}
        )
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    # проверить существует ли запрашиваемый автор
    follow = get_object_or_404(User, id=user_id)
    following = Follow.objects.filter(user=request.user, following=follow)
    if not following.exists():
        return Response(
            {'errors': 'Запрашиваемой подписки не сущестовало!'},
            status=status.HTTP_400_BAD_REQUEST
        )
    following.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)


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


class FollowViewSet(viewsets.ModelViewSet):
    http_method_names = ['get']
    serializer_class = FollowSerializer
    pagination_class = LimitOffsetPagination
    queryset = User.objects.all()
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        followings = Follow.objects.filter(user_id=self.request.user.id)
        return User.objects.filter(
            id__in=followings.values_list('following')
        )
