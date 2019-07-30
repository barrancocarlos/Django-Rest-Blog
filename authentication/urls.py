from django.urls import path, include
from rest_framework import routers
from rest_framework.routers import DefaultRouter
from . import views
from .views import ProfileViewSet
from rest_framework_jwt.views import obtain_jwt_token, refresh_jwt_token, verify_jwt_token

router = routers.DefaultRouter()
router.register(r'profiles', ProfileViewSet, base_name='profiles')

urlpatterns = [
    path('login/', obtain_jwt_token),
    path('token-refresh/', refresh_jwt_token),
    path('token-verify/', verify_jwt_token),
]


