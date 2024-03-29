# accounts/api/urls.py
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from django.urls import path, include
from rest_framework import routers
from knox.views import LogoutView

from .views import UserAPIView, RegisterAPIView, LoginAPIView, UserPerfilViewSet#PerfilViewSet
router = routers.DefaultRouter()
router.register(r'userperfil', UserPerfilViewSet)
urlpatterns = [
    path('', include('knox.urls')),
    path('', include(router.urls)),
    path('user/', UserAPIView.as_view()),
    path('register/', RegisterAPIView.as_view()),
    path('login/', LoginAPIView.as_view()),
    path('logout/', LogoutView.as_view(), name='knox_logout'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]