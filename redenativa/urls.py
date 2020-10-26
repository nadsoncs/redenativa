"""redenativa URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from app.api import (
    AceiteTermoViewSet, 
    OrganizacaoViewSet, 
    LocalidadeViewSet, 
    OrgRegisterAPIView,
    OrgMinAPIView, 
    ASOfertaViewSet, 
    ItemOfertaViewSet,
    AsoItemViewSet,
    AsdItemViewSet,
    ItemDemandaViewSet, 
    ItemAPIView, 
    CategoriaAPIView, 
    TipoTerritorioAPIView,
    MyOrganizacaoAPIView,
    ASDemandaViewSet,
    IndicacaoAPIView,
    CoordenadaViewSet,
    LocalidadeCoordenadasViewSet,
    ASDemandaCoordenadasAPIView,
    ASOfertaCoordenadasAPIView
)
#Arquivos estáticos
from django.conf import settings
from django.conf.urls.static import static
####################

router = routers.DefaultRouter()
router.register(r'aceitetermo', AceiteTermoViewSet)
router.register(r'organizacao', OrganizacaoViewSet)
router.register(r'localidade', LocalidadeViewSet)
router.register(r'asoferta', ASOfertaViewSet)
router.register(r'itemoferta', ItemOfertaViewSet)
router.register(r'asdemanda', ASDemandaViewSet)
router.register(r'itemdemanda', ItemDemandaViewSet)
router.register(r'asoitem', AsoItemViewSet)
router.register(r'asditem', AsdItemViewSet)
router.register(r'coordenadas', CoordenadaViewSet)
router.register(r'localidade-coordenadas', LocalidadeCoordenadasViewSet)
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('api/auth/', include('accounts.api.urls')),
    path('orgcreate/', OrgRegisterAPIView.as_view()),
    path('orgmin/', OrgMinAPIView.as_view()),
    path('item/', ItemAPIView.as_view()),
    path('categoria/', CategoriaAPIView.as_view()),
    path('territorio/', TipoTerritorioAPIView.as_view()),
    path('myorg/', MyOrganizacaoAPIView.as_view()),
    path('indicacao/', IndicacaoAPIView.as_view()),
    path('asdemanda-coord/', ASDemandaCoordenadasAPIView.as_view()),
    path('asoferta-coord/', ASOfertaCoordenadasAPIView.as_view()),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)