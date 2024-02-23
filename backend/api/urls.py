from api.views import (
    IngreViewSet, RecipesViewSet, TagViewSet,
    ProfileViewSet, create_subscribe
)
from django.urls import include, path
from rest_framework import routers


router = routers.DefaultRouter()
router.register(r'ingredients', IngreViewSet, basename='Ingredients')
router.register(r'recipes', RecipesViewSet, basename='Recipes')
router.register(r'tags', TagViewSet, basename='Tags')
# router.register('users/subscriptions', FollowViewSet, basename='Followings')
router.register(r'users', ProfileViewSet, basename='Users')


urlpatterns = [
    path('', include(router.urls)),
    path('', include('djoser.urls')),
    path("auth/", include("djoser.urls.authtoken")),
    path("users/<user_id>/subscribe/", create_subscribe),
]
