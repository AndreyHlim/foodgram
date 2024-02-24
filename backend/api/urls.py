from api.views import (
    IngreViewSet, RecipesViewSet, TagViewSet,
)
from django.urls import include, path
from rest_framework import routers


router_v1 = routers.DefaultRouter()
router_v1.register(r'ingredients', IngreViewSet, basename='Ingredients')
router_v1.register(r'recipes', RecipesViewSet, basename='Recipes')
router_v1.register(r'tags', TagViewSet, basename='Tags')


urlpatterns = [
    path('', include(router_v1.urls)),
    path('', include('users.urls')),
]
