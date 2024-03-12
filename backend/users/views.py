from api.permissions import AuthorStaffOrReadOnly
from api.serializers import FollowSerializer, ProfileSerializer
from djoser.views import UserViewSet
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from users.models import Follow, User

from django.shortcuts import get_object_or_404


class ProfileViewSet(UserViewSet):
    http_method_names = ['get', 'post', 'delete']
    pagination_class = LimitOffsetPagination
    serializer_class = ProfileSerializer

    def get_permissions(self):
        if self.action == 'me':
            return (IsAuthenticated(),)
        if self.action in ['subscribe', 'delete_subscribe']:
            return (AuthorStaffOrReadOnly(),)
        return (AllowAny(),)

    @action(
        detail=False,
        methods=['get'],
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
        methods=['post'],
    )
    def subscribe(self, request, id):
        follow = get_object_or_404(User, id=id)

        request.data['email'] = follow.email
        request.data['username'] = follow.username
        request.data['first_name'] = follow.first_name
        request.data['last_name'] = follow.last_name

        serializer = FollowSerializer(
            follow,
            data=request.data,
            context={"request": request}
        )
        if serializer.is_valid():
            Follow.objects.create(
                user=request.user,
                following=follow,
            )
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @subscribe.mapping.delete
    def delete_subscribe(self, request, id):
        following = Follow.objects.filter(
            user=request.user,
            following=get_object_or_404(User, id=id)
        )
        if not following.exists():
            return Response(
                {'errors': 'Запрашиваемой подписки не сущестовало!'},
                status=status.HTTP_400_BAD_REQUEST
            )
        following.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
