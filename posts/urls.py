from django.urls import path, include
from rest_framework import routers
from rest_framework.routers import DefaultRouter
from . import views

router = routers.DefaultRouter()
router.register(r'authors', views.AuthorViewset)
router.register(r'posts', views.PostViewset)

urlpatterns = [
    path(r'api/', include(router.urls)),      
]