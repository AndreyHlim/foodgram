from rest_framework.decorators import (
    api_view, permission_classes as dec_permission_classes
)
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from rest_framework.exceptions import ValidationError
from users.models import Follow
from django.contrib.auth import get_user_model
from django.db import IntegrityError
from api.serializers import FollowSerializer
from rest_framework.response import Response
from rest_framework import status


User = get_user_model()


@api_view(['POST', 'DELETE'])
@dec_permission_classes([IsAuthenticated])
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

    else:
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
