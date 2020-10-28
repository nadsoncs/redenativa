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
    Encontro,
    Indicacao
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

class CoordenadaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Coordenada
        #fields = ['latitude', 'longitude', 'raio']
        fields = '__all__'
        read_only_fields = ['id', 'raio']

class CoordenadaAuxSerializer(serializers.ModelSerializer):
    class Meta:
        model = Coordenada
        fields = ['latitude', 'longitude', 'raio']
        #fields = '__all__'
        read_only_fields = ['id', 'raio']

class LocalidadeCoordenadasSerializer(serializers.ModelSerializer):
    coordenada = CoordenadaAuxSerializer()
    class Meta:
        model = Localidade
        fields = ['id', 'estado', 'cidade', 'bairro', 'cep', 'tipo', 'coordenada']
        read_only_fields = ['id']
    def create(self, validated_data):
        localidade_data = validated_data.pop('localidade')
        localidade = Localidade.objects.create(**localidade_data)
        coordenada = Coordenada.objects.create(localidade=localidade, **validated_data)
        return organizacao

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

class OrganizacaoCoordenadasSerializer(serializers.ModelSerializer):
    localidade = LocalidadeCoordenadasSerializer()
    class Meta:
        model = Organizacao
        fields = ['id','name', 'tipo', 'email', 'tel', 'localidade', 'logo']

class OrgMimSerializer(serializers.ModelSerializer):
    class Meta:
        model = Organizacao
        #fields = '__all__'
        fields = ['id','name']
        read_only_fields = ['id', 'name']

class OrgFullSerializer(serializers.ModelSerializer):
    organizacao = OrganizacaoSerializer()
    user = RegisterSerializer()
    perfil = PerfilSerializer()
    aceite = AceiteTermoSerializer()
    class Meta:
        model = Representante
        fields = ['user','perfil', 'cargo','organizacao', 'aceite']
    
    def create(self, validated_data):
        organizacao_data = validated_data.pop('organizacao')
        localidade_data = organizacao_data.pop('localidade')
        localidade = Localidade.objects.create(**localidade_data)
        organizacao = Organizacao.objects.create(localidade=localidade, **organizacao_data)
        perfil_data = validated_data.pop('perfil')
        user_data = validated_data.pop('user')
        user = User.objects.create_user(is_active=False, **user_data)
        perfil = Perfil.objects.create(user=user, **perfil_data)
        aceite_data = validated_data.pop('aceite')
        aceite = AceiteTermo.objects.create(user=user, **aceite_data)
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
    class Meta:
        model = ItemAcaoOferta
        fields = ['id', 'a_s_oferta', 'item', 'qtd_inicial', 'saldo']
        read_only_fields = ['id', 'saldo', 'a_s_oferta']
    def create(self, validated_data):
        saldo = validated_data['qtd_inicial']
        item_acao = ItemAcaoOferta.objects.create(saldo=saldo, **validated_data)
        return item_acao

class ASOfertaSerializer(serializers.ModelSerializer):
    localidade = LocalidadeCoordenadasSerializer()
    class Meta:
        model = AcaoSolidariaOferta
        #fields = '__all__'
        fields = ['id','name', 'descricao', 'is_covid', 'data', 'validade', 'organizacao', 'categoria', 'localidade']
        read_only_fields = ['id', 'organizacao']
    def create(self, validated_data):
        user =  self.context['request'].user
        organizacao = Organizacao.objects.get(representante__user = user)
        localidade_data = validated_data.pop('localidade')
        coordenada_data = localidade_data.pop('coordenada')
        localidade = Localidade.objects.create(**localidade_data)
        coordenada = Coordenada.objects.create(localidade, **localidade_coordenada_data)
        acao_oferta = AcaoSolidariaOferta.objects.create(organizacao=organizacao, localidade=localidade, **validated_data)
        return acao_oferta
#Ação Solidária de Oferta + Itens
class AsoItemSerializer(serializers.ModelSerializer):
    localidade = LocalidadeCoordenadasSerializer()
    itens_acao = ItemOfertaSerializer(many=True)
    class Meta:
        model = AcaoSolidariaOferta
        #fields = '__all__'
        fields = ['id','name', 'descricao', 'is_covid', 'data', 'validade', 'organizacao', 'categoria', 'localidade', 'itens_acao']
        read_only_fields = ['id', 'organizacao']
    def create(self, validated_data):
        user =  self.context['request'].user
        organizacao = Organizacao.objects.get(representante__user = user)
        itens_acao_data = validated_data.pop('itens_acao')
        localidade_data = validated_data.pop('localidade')
        coordenada_data = localidade_data.pop('coordenada')
        localidade = Localidade.objects.create(**localidade_data)
        coordenada = Coordenada.objects.create(localidade, **localidade_coordenada_data)
        acao_oferta = AcaoSolidariaOferta.objects.create(organizacao=organizacao, localidade=localidade, **validated_data)
        for item_acao_data in itens_acao_data:
            saldo = item_acao_data['qtd_inicial']
            ItemAcaoOferta.objects.create(a_s_oferta=acao_oferta, saldo=saldo, **item_acao_data)
        return acao_oferta

class ASDemandaSerializer(serializers.ModelSerializer):
    class Meta:
        model = AcaoSolidariaDemanda
        #fields = '__all__'
        fields = ['id','name', 'descricao', 'is_covid', 'num_familias','data', 'validade', 'organizacao', 'categoria']
        read_only_fields = ['id', 'organizacao']
    def create(self, validated_data):
        user =  self.context['request'].user
        organizacao = Organizacao.objects.get(representante__user = user)
        acao_demanda = AcaoSolidariaDemanda.objects.create(organizacao=organizacao, **validated_data)
        return acao_demanda

class ASOfertaCoordenadasSerializer(serializers.ModelSerializer):
    organizacao = OrganizacaoSerializer()
    localidade = LocalidadeCoordenadasSerializer()
    class Meta:
        model = AcaoSolidariaOferta
        #fields = '__all__'
        fields = ['id','name', 'descricao', 'is_covid', 'data', 'validade', 'organizacao', 'categoria', 'localidade']

class ASDemandaCoordenadasSerializer(serializers.ModelSerializer):
    organizacao = OrganizacaoCoordenadasSerializer()
    class Meta:
        model = AcaoSolidariaDemanda
        #fields = '__all__'
        fields = ['id','name', 'descricao', 'is_covid', 'num_familias','data', 'validade', 'organizacao', 'categoria']

class ItemDemandaSerializer(serializers.ModelSerializer):
    class Meta:
        model = ItemAcaoDemanda
        #fields = '__all__'
        fields = ['id', 'a_s_demanda', 'item', 'qtd_inicial', 'saldo']
        read_only_fields = ['id', 'saldo', 'a_s_demanda']
    def create(self, validated_data):
        saldo = validated_data['qtd_inicial']
        item_acao = ItemAcaoDemanda.objects.create(saldo=saldo, **validated_data)
        return item_acao

#Ação Solidária de Oferta + Itens
class AsdItemSerializer(serializers.ModelSerializer):
    itens_acao = ItemDemandaSerializer(many=True)
    class Meta:
        model = AcaoSolidariaDemanda
        #fields = '__all__'
        fields = ['id','name', 'descricao', 'is_covid', 'num_familias', 'data', 'validade', 'organizacao', 'categoria', 'itens_acao']
        read_only_fields = ['id', 'organizacao']
    def create(self, validated_data):
        user =  self.context['request'].user
        organizacao = Organizacao.objects.get(representante__user = user)
        itens_acao_data = validated_data.pop('itens_acao')
        acao_demanda = AcaoSolidariaDemanda.objects.create(organizacao=organizacao, **validated_data)
        for item_acao_data in itens_acao_data:
            saldo = item_acao_data['qtd_inicial']
            ItemAcaoDemanda.objects.create(a_s_demanda=acao_demanda, saldo=saldo, **item_acao_data)
        return acao_demanda

class EncontroSerializer(serializers.ModelSerializer):
    class Meta:
        model = Encontro
        fields = '__all__'

class IndicacaoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Indicacao
        fields = ['myname', 'email', 'myfone', 'organizacao', 'email_org', 'tel_org', 'acao_solidaria', 'descrição']
        #fields = '__all__'

