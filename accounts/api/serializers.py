# accounts/api/serializers.py

from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from accounts.models import Perfil
from rest_framework import serializers

User._meta.get_field('email')._unique = True


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name']

class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name','username', 'email', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(
            validated_data['username'],
            validated_data['email'],
            validated_data['password'],
            validated_data['first_name'],
            validated_data['last_name']
        )
        return user


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

    def validate(self, data):
        user = authenticate(**data)
        if user and user.is_active:
            return user
        raise serializers.ValidationError("Incorrect Credentials")
"""
class PerfilSerializer(serializers.ModelSerializer):
    user = RegisterSerializer()
    class Meta:
        model = Perfil
        #fields = '__all__'
        fields =  ['id','cpf', 'tel','user']
        read_only_fields = ['id']
"""
class PerfilSerializer(serializers.ModelSerializer):
    class Meta:
        model = Perfil
        #fields = '__all__'
        fields =  ['id','cpf', 'tel']
        read_only_fields = ['id']

class UserPerfilSerializer(serializers.ModelSerializer):
    perfil = PerfilSerializer()
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'perfil']
        read_only_fields = ['id']
    
    def update(self, instance, validated_data):
        perfil_data = validated_data.pop('perfil')
        perfil = instance.perfil

        instance.username = validated_data.get('username', instance.username)
        instance.email = validated_data.get('email', instance.email)
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.save()

        perfil.cpf = perfil_data.get('cpf', perfil.cpf)
        perfil.tel = perfil_data.get('tel', perfil.tel)
        perfil.save()

        return instance
"""
        profile.is_premium_member = profile_data.get(
            'is_premium_member',
            profile.is_premium_member
        )
        profile.has_support_contract = profile_data.get(
            'has_support_contract',
            profile.has_support_contract
         )
         """
        
"""    
    def update(self, instance, validated_data):
        instance.title = validated_data.get('title', instance.title)
        instance.code = validated_data.get('code', instance.code)
        instance.linenos = validated_data.get('linenos', instance.linenos)
        instance.language = validated_data.get('language', instance.language)
        instance.style = validated_data.get('style', instance.style)
        instance.save()
        return instance
"""