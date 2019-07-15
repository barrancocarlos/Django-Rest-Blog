from django.urls import path, include
from rest_framework import routers
from rest_framework.routers import DefaultRouter
from . import views
from .views import ProfileViewSet


urlpatterns = [

]

router = routers.DefaultRouter()
router.register(r'profiles', ProfileViewSet, base_name='profiles')
