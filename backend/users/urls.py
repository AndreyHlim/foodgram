from django.urls import include, path
from rest_framework import routers
from users.views import ProfileViewSet

router = routers.DefaultRouter()
router.register(r'users', ProfileViewSet, basename='Users')

urlpatterns = [
    path('', include(router.urls)),
    path('', include('djoser.urls')),
    path("auth/", include("djoser.urls.authtoken")),
    # path("users/<user_id>/subscribe/", create_subscribe),
]
