from rest_framework import viewsets, generics, permissions
from dry_rest_permissions.generics import DRYPermissions, DRYObjectPermissions
from rest_framework.response import Response
from accounts.api.serializers import UserSerializer
from django.shortcuts import get_object_or_404
#from rest_framework.permissions import BasePermission, IsAuthenticated, SAFE_METHODS
from app.models import (
    TermoUso, 
    AceiteTermo, 
    Organizacao, 
    Localidade, 
    AcaoSolidariaOferta, 
    ItemAcaoOferta, 
    ItemAcaoDemanda, 
    AcaoSolidariaDemanda, 
    Item, 
    Categoria, 
    TipoTerritorio, 
    Representante,
    Indicacao
)
from app.serializers import (
    AceiteTermoSerializer, 
    OrganizacaoSerializer, 
    LocalidadeSerializer, 
    OrgFullSerializer, 
    ASOfertaSerializer,
    ASDemandaSerializer, 
    ItemOfertaSerializer,
    ItemDemandaSerializer, 
    ItemSerializer, 
    CategoriaSerializer, 
    TipoTerritorioSerializer,
    RepresentanteSerializer,
    IndicacaoSerializer
)


class AceiteTermoViewSet (viewsets.ModelViewSet):
    permission_classes = (DRYObjectPermissions,)
    queryset = AceiteTermo.objects.all()
    serializer_class = AceiteTermoSerializer
    def get_queryset(self):
        user = self.request.user
        return AceiteTermo.objects.filter(user=user)

class LocalidadeViewSet(viewsets.ModelViewSet):
    serializer_class = LocalidadeSerializer
    queryset = Localidade.objects.all()


class OrganizacaoViewSet(viewsets.ModelViewSet):
    serializer_class = RepresentanteSerializer
    queryset = Organizacao.objects.all()

class MyOrganizacaoAPIView(generics.RetrieveUpdateAPIView):
#class MyOrganizacaoViewSet(viewsets.ModelViewSet):
    serializer_class = RepresentanteSerializer
    queryset = Representante.objects.all()
    def get_object(self):
        user = self.request.user
        return get_object_or_404(Representante, user=user)

class ItemAPIView(generics.ListCreateAPIView):
    serializer_class = ItemSerializer
    queryset = Item.objects.all()

class CategoriaAPIView(generics.ListCreateAPIView):
    serializer_class = CategoriaSerializer
    queryset = Categoria.objects.all()

class TipoTerritorioAPIView(generics.ListCreateAPIView):
    serializer_class = TipoTerritorioSerializer
    queryset = TipoTerritorio.objects.all()

class OrgRegisterAPIView(generics.CreateAPIView):
    serializer_class = OrgFullSerializer
    permission_classes = (permissions.AllowAny,)
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        representante = serializer.save()
        return Response({
            "user": UserSerializer(representante.user, context=self.get_serializer_context()).data,
            "organizacao": OrganizacaoSerializer(representante.organizacao, context=self.get_serializer_context() ).data,
        })

class ASOfertaViewSet(viewsets.ModelViewSet):
    serializer_class = ASOfertaSerializer
    queryset = AcaoSolidariaOferta.objects.all()

class ItemOfertaViewSet(viewsets.ModelViewSet):
    serializer_class = ItemOfertaSerializer
    queryset = ItemAcaoOferta.objects.all()

class ItemDemandaViewSet(viewsets.ModelViewSet):
    serializer_class = ItemDemandaSerializer
    queryset = ItemAcaoDemanda.objects.all()

class ASDemandaViewSet(viewsets.ModelViewSet):
    serializer_class = ASDemandaSerializer
    queryset = AcaoSolidariaDemanda.objects.all()

class IndicacaoAPIView(generics.CreateAPIView):
    serializer_class = IndicacaoSerializer
    permission_classes = (permissions.AllowAny,)
    queryset = Indicacao.objects.all()