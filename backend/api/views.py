from api.serializers import (IngreSerializer, RecipeLittleSerializer,
                             RecipesSerializer, TagSerializer)
from django.contrib.auth import get_user_model
from django.db.models import Sum
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from recipes.models import (AmountIngredients, Favourite, Ingredient, Recipe,
                            ShoppingCart, Tag)
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from .paginators import PageLimitPagination
from .permissions import AuthorStaffOrReadOnly

User = get_user_model()


class IngreViewSet(viewsets.ModelViewSet):
    serializer_class = IngreSerializer
    http_method_names = ['get']
    pagination_class = None
    permission_classes = (AllowAny,)

    def get_queryset(self):
        queryset = Ingredient.objects.all()
        name = self.request.query_params.get('name')
        if name is not None:
            return queryset.filter(name__startswith=name)
        return queryset


class RecipesViewSet(viewsets.ModelViewSet):
    serializer_class = RecipesSerializer
    permission_classes = (AuthorStaffOrReadOnly,)
    http_method_names = ['get', 'post', 'patch', 'delete']
    pagination_class = PageLimitPagination
    queryset = Recipe.objects.all().order_by('-id')
    filter_backends = (DjangoFilterBackend,)

    def get_queryset(self):
        queryset = self.queryset
        tags = self.request.query_params.getlist('tags')
        author = self.request.query_params.get('author')
        favourite = self.request.query_params.get('is_favorited')
        shopping = self.request.query_params.get('is_in_shopping_cart')
        if tags != []:
            queryset = queryset.filter(tags__slug__in=tags).distinct('id')
        if author is not None:
            queryset = queryset.filter(author=author)
        if favourite is not None:
            user = self.request.user
            if user.is_anonymous:
                return queryset
            if int(favourite) == 1:
                return queryset.filter(favorites__user=user)
            return queryset.exclude(favorites__user=user)
        if shopping is not None:
            user = self.request.user
            if user.is_anonymous:
                return queryset
            if int(shopping) == 1:
                return queryset.filter(shopping__user=user)
            return queryset.exclude(shopping__user=user)
        return queryset

    @action(
        detail=True,
        methods=['post', 'delete'],
        permission_classes=[IsAuthenticated]
    )
    def favorite(self, request, pk):

        if request.method == 'POST':
            if not Recipe.objects.filter(id=pk).exists():
                return Response(
                    {'errors': 'Рецепта не существует!'},
                    status=status.HTTP_400_BAD_REQUEST
                )

            recipe = Recipe.objects.get(id=pk)
            user = request.user

            if Favourite.objects.filter(
                user=user, recipe=recipe
            ).exists():
                return Response(
                    {'errors': 'Рецепт уже добавлен!'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            Favourite.objects.create(user=user, recipe=recipe)
            serializer = RecipeLittleSerializer(recipe)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        recipe = get_object_or_404(Recipe, id=pk)
        user = request.user

        favourite = Favourite.objects.filter(user=user, recipe__id=pk)
        if favourite.exists():
            favourite.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(
            {'errors': f'Рецепт не в избранном пользователя {user}!'},
            status=status.HTTP_400_BAD_REQUEST
        )

    @action(
        detail=True,
        methods=['post', 'delete'],
        permission_classes=[IsAuthenticated]
    )
    def shopping_cart(self, request, pk):

        if request.method == 'POST':
            if not Recipe.objects.filter(id=pk).exists():
                return Response(
                    {'errors': 'Рецепта не существует!'},
                    status=status.HTTP_400_BAD_REQUEST
                )

            recipe = Recipe.objects.get(id=pk)
            user = request.user
            if ShoppingCart.objects.filter(
                user=user, recipe=recipe
            ).exists():
                return Response(
                    {'errors': 'Рецепт уже добавлен к спису покупок!'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            ShoppingCart.objects.create(user=user, recipe=recipe)
            serializer = RecipeLittleSerializer(recipe)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        recipe = get_object_or_404(Recipe, id=pk)
        user = request.user
        shop_recipe = ShoppingCart.objects.filter(user=user, recipe__id=pk)
        if shop_recipe.exists():
            shop_recipe.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(
            {'errors': f'Рецепт не в списке покупок у "{user}"!'},
            status=status.HTTP_400_BAD_REQUEST
        )

    @action(
        detail=False,
        methods=['get'],
        permission_classes=[IsAuthenticated]
    )
    def download_shopping_cart(self, request):
        user = request.user
        if not user.shopping.exists():
            return Response(status=status.HTTP_400_BAD_REQUEST)

        ingredients = AmountIngredients.objects.filter(
            recipe__shopping__user=request.user
        ).values(
            'ingredient__name',
            'ingredient__measurement_unit'
        ).annotate(amount=Sum('amount'))
        shopping_list = (
            f'Список покупок для: {user.get_full_name()}\n\n'
        )
        shopping_list += '\n'.join([
            f'- {ingredient["ingredient__name"]} '
            f'({ingredient["ingredient__measurement_unit"]})'
            f' - {ingredient["amount"]}'
            for ingredient in ingredients
        ])

        filename = f'{user.username}_shopping_list.txt'
        response = HttpResponse(shopping_list, content_type='text/plain')
        response['Content-Disposition'] = f'attachment; filename={filename}'
        return response


class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = (AllowAny,)
    pagination_class = None
    http_method_names = ['get']
