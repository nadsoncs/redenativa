from django.contrib import admin
from accounts.models import Perfil
# Register your models here.
class PerfilAdmin(admin.ModelAdmin):
    list_display = ['user', 'tel', 'cpf']
    search_fields = ['user']

admin.site.register(Perfil, PerfilAdmin)