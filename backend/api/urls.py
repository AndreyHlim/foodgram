from api.views import IngredientViewSet, RecipesViewSet, TagViewSet
from rest_framework import routers

from django.urls import include, path

router_v1 = routers.DefaultRouter()
router_v1.register(r'ingredients', IngredientViewSet, basename='Ingredients')
router_v1.register(r'recipes', RecipesViewSet, basename='Recipes')
router_v1.register(r'tags', TagViewSet, basename='Tags')


urlpatterns = [
    path('', include(router_v1.urls)),
    path('', include('users.urls')),
]
