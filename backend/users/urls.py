from rest_framework import routers
from users.views import ProfileViewSet

from django.urls import include, path

router = routers.DefaultRouter()
router.register(r'users', ProfileViewSet, basename='Users')

urlpatterns = [
    path('', include(router.urls)),
    path('', include('djoser.urls')),
    path("auth/", include("djoser.urls.authtoken")),
]
