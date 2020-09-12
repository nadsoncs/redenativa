from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class Perfil(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    tel = models.CharField(max_length=15, verbose_name='telefone')
    cpf = models.CharField(max_length=11, verbose_name='CPF')
    class Meta:
        verbose_name = 'Perfil'
        verbose_name_plural = 'Perfis'
    def __str__(self):
        return "%s %s" % (self.user.first_name, self.user.last_name)