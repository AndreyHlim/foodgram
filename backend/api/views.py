from api.filters import IngredientSearchFilter, RecipeFilter
from api.func import create_dependence, delete_dependence
from api.paginators import PageLimitPagination
from api.permissions import AuthorStaffOrReadOnly
from api.serializers import (
    IngredientSerializer,
    RecipeLittleSerializer,
    RecipesSerializer,
    TagSerializer
)
from django_filters.rest_framework import DjangoFilterBackend
from recipes.models import (
    AmountIngredients,
    Favourite,
    Ingredient,
    Recipe,
    ShoppingCart,
    Tag
)
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from django.contrib.auth import get_user_model
from django.db.models import Sum
from django.http import HttpResponse

User = get_user_model()


class IngredientViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    pagination_class = None
    permission_classes = (AllowAny, )
    filter_backends = (IngredientSearchFilter, )
    search_fields = ('^name', )


class RecipesViewSet(viewsets.ModelViewSet):
    serializer_class = RecipesSerializer
    permission_classes = (AuthorStaffOrReadOnly, )
    http_method_names = ('get', 'post', 'patch', 'delete')
    pagination_class = PageLimitPagination
    queryset = Recipe.objects.all().order_by(
        '-id',
    ).select_related(
        'author',
    ).prefetch_related(
        'ingredients', 'tags',
    )
    filter_backends = (DjangoFilterBackend, )
    filterset_class = RecipeFilter

    @action(
        detail=True,
        methods=['post'],
        permission_classes=[IsAuthenticated]
    )
    def favorite(self, request, pk):
        return create_dependence(
            RecipeLittleSerializer, Favourite, request.user, pk
        )

    @favorite.mapping.delete
    def delete_favorite(self, request, pk):
        return delete_dependence(Favourite, request.user, pk)

    @action(
        detail=True,
        methods=['post'],
        permission_classes=[IsAuthenticated]
    )
    def shopping_cart(self, request, pk):
        return create_dependence(
            RecipeLittleSerializer, ShoppingCart, request.user, pk
        )

    @shopping_cart.mapping.delete
    def delete_shopping_cart(self, request, pk):
        return delete_dependence(ShoppingCart, request.user, pk)

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
        response = HttpResponse(
            shopping_list,
            content_type="text.txt; charset=utf-8"
        )
        response['Content-Disposition'] = f'attachment; filename={filename}'
        return response


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = (AllowAny,)
    pagination_class = None
