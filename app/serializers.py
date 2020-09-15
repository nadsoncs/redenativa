from django.contrib.auth.models import User
from accounts.models import Perfil
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator
from accounts.api.serializers import UserSerializer, RegisterSerializer, PerfilSerializer
from app.models import (
    TermoUso, 
    AceiteTermo, 
    TipoTerritorio, 
    Localidade, 
    Coordenada, 
    Organizacao, 
    Representante, 
    AcaoSolidariaOferta, 
    Categoria, 
    AcaoSolidariaDemanda, 
    Item,
    ItemAcaoOferta,
    ItemAcaoDemanda,
    Encontro
)


class AceiteTermoSerializer (serializers.ModelSerializer):
    class Meta:
        model = AceiteTermo
        fields = ['id','termo', 'user']
        read_only_fields = ['id','user']
        extra_kwargs = {
            'user': {
                'default': serializers.CreateOnlyDefault(
                    serializers.CurrentUserDefault()
                ),
            }
        }
        validators = [
            UniqueTogetherValidator(
                queryset= AceiteTermo.objects.all(),
                fields=['termo', 'user'],
                message='Este usuário já aceitou este Termo de Uso anteriormente',
            )
        ]
  
    def create(self, validated_data):
        user =  self.context['request'].user
        aceite = AceiteTermo.objects.create(user=user, **validated_data)
        return aceite

class LocalidadeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Localidade
        fields = '__all__'

class OrganizacaoSerializer(serializers.ModelSerializer):
    localidade = LocalidadeSerializer()
    class Meta:
        model = Organizacao
        #fields = '__all__'
        fields = ['id','name', 'tipo', 'email', 'tel', 'localidade', 'logo']
        read_only_fields = ['id']
    def create(self, validated_data):
        localidade_data = validated_data.pop('localidade')
        localidade = Localidade.objects.create(**localidade_data)
        organizacao = Organizacao.objects.create(localidade=localidade, **validated_data)
        return organizacao

class OrgFullSerializer(serializers.ModelSerializer):
    organizacao = OrganizacaoSerializer()
    user = RegisterSerializer()
    perfil = PerfilSerializer()
    class Meta:
        model = Representante
        fields = ['user','perfil', 'cargo','organizacao']
    
    def create(self, validated_data):
        organizacao_data = validated_data.pop('organizacao')
        localidade_data = organizacao_data.pop('localidade')
        localidade = Localidade.objects.create(**localidade_data)
        organizacao = Organizacao.objects.create(localidade=localidade, **organizacao_data)
        perfil_data = validated_data.pop('perfil')
        user_data = validated_data.pop('user')
        user = User.objects.create_user(is_active=False, **user_data)
        perfil = Perfil.objects.create(user=user, **perfil_data)
        representante = Representante.objects.create(organizacao=organizacao, user=user, **validated_data)
        return representante

class RepresentanteSerializer(serializers.ModelSerializer):
    organizacao = OrganizacaoSerializer()
    class Meta:
        model = Representante
        fields = ['user', 'cargo', 'organizacao']
        read_only_fields = ['user']
    
    def update(self, instance, validated_data):
        organizacao_data = validated_data.pop('organizacao')
        localidade_data = organizacao_data.pop('localidade')
        
        organizacao = instance.organizacao
        localidade = instance.organizacao.localidade
        
        instance.cargo = validated_data.get('cargo', instance.cargo)

        organizacao.name = organizacao_data.get('name', organizacao.name)
        organizacao.tipo = organizacao_data.get('tipo', organizacao.tipo)
        organizacao.email = organizacao_data.get('email', organizacao.email)
        organizacao.tel = organizacao_data.get('tel', organizacao.tel)
        organizacao.logo = organizacao_data.get('logo', organizacao.logo)
        organizacao.save()

        localidade.estado = localidade_data.get('estado', localidade.estado)
        localidade.cidade = localidade_data.get('cidade', localidade.cidade)
        localidade.bairro = localidade_data.get('bairro', localidade.bairro)
        localidade.cep = localidade_data.get('cep', localidade.cep)
        localidade.tipo = localidade_data.get('tipo', localidade.tipo)
        localidade.save()

        return instance

class CategoriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categoria
        fields = ['id', 'name']
        read_only_fields = ['id']
        #fields = '__all__'
class TipoTerritorioSerializer(serializers.ModelSerializer):
    class Meta:
        model = TipoTerritorio
        fields = ['id', 'name']
        read_only_fields = ['id']

class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = '__all__'

class ItemOfertaSerializer(serializers.ModelSerializer):
    #item = ItemSerializer(many=True)
    class Meta:
        model = ItemAcaoOferta
        fields = ['a_s_oferta', 'item', 'qtd_inicial']
        #fields = '__all__'
    """
    def create(self, validated_data):
        itens_data = validated_data.pop('item')
        for item_data in itens_data:
            Item.objects.create(**itens_data)
    """
class ASOfertaSerializer(serializers.ModelSerializer):
    """
    Colocar a organização de forma dinâmica baseada no usuário logado
    """
    localidade = LocalidadeSerializer()
    class Meta:
        model = AcaoSolidariaOferta
        #fields = '__all__'
        fields = ['name', 'descricao', 'is_covid', 'data', 'validade', 'organizacao', 'categoria', 'localidade']
        read_only_fields = ['id', 'organizacao']
    def create(self, validated_data):
        user =  self.context['request'].user
        organizacao = Organizacao.objects.get(representante__user = user)
        localidade_data = validated_data.pop('localidade')
        localidade = Localidade.objects.create(**localidade_data)
        acao_oferta = AcaoSolidariaOferta.objects.create(organizacao=organizacao, localidade=localidade, **validated_data)
        return acao_oferta
    
class ASDemandaSerializer(serializers.ModelSerializer):
    class Meta:
        model = AcaoSolidariaDemanda
        fields = '__all__'

class ItemDemandaSerializer(serializers.ModelSerializer):
    class Meta:
        model = ItemAcaoDemanda
        fields = '__all__'

class EncontroSerializer(serializers.ModelSerializer):
    class Meta:
        model = Encontro
        fields = '__all__'
