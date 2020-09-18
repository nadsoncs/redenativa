from django.contrib import admin
from app.models import (
#    Perfil,
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
# Register your models here.
"""class PerfilAdmin(admin.ModelAdmin):
    list_display = ['user', 'tel', 'cpf']
    search_fields = ['user']"""

class TermoUsoAdmin(admin.ModelAdmin):
    list_display = ['arquivo', 'data', 'is_active']
    list_filter = ['is_active']

class AceiteTermoAdmin(admin.ModelAdmin):
    list_display = ['user', 'termo']
    list_filter = ['user']

class TipoTerritorioAdmin(admin.ModelAdmin):
    list_display = ['name', 'is_active', 'is_new']
    search_fields = ['name']
    list_filter = ['is_active', 'is_new']

class LocalidadeAdmin(admin.ModelAdmin):
    list_display = ['estado', 'cidade', 'bairro']
    search_fields = ['estado', 'cidade']

class CoordenadaAdmin(admin.ModelAdmin):
    list_display = ['latitude', 'longitude', 'raio']

class OrganizacaoAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'tel', 'is_active']
    search_fields = ['name']
    list_filter = ['is_active']

class RepresentanteAdmin(admin.ModelAdmin):
    list_display = ['cargo', 'user', 'organizacao']

class AcaoSolidariaOfertaAdmin(admin.ModelAdmin):
    list_display = ['name', 'descricao', 'organizacao', 'categoria', 'validade','is_covid']
    search_fields = ['name', 'descricao', 'organizacao']
    list_filter = ['categoria', 'is_covid']

class AcaoSolidariaDemandaAdmin(admin.ModelAdmin):
    list_display = ['name', 'descricao', 'organizacao', 'categoria', 'validade','num_familias', 'is_covid']
    search_fields = ['name', 'descricao', 'organizacao']
    list_filter = ['categoria', 'is_covid']

class CategoriaAdmin(admin.ModelAdmin):
    list_display = ['name', 'is_active', 'is_new']
    list_filter = ['is_active', 'is_new']

class ItemAdmin(admin.ModelAdmin):
    list_display = ['name', 'un_medida']
    list_filter = ['un_medida']

class ItemAcaoOfertaAdmin(admin.ModelAdmin):
    list_display = ['a_s_oferta', 'item', 'qtd_inicial', 'saldo', 'data']
    list_filter = ['a_s_oferta']

class ItemAcaoDemandaAdmin(admin.ModelAdmin):
    list_display = ['a_s_demanda', 'item', 'qtd_inicial', 'saldo', 'data']
    list_filter = ['a_s_demanda']

class EncontroAdmin(admin.ModelAdmin):
    list_display = ['item_oferta', 'item_demanda', 'is_total', 'data']
    list_filter = ['item_oferta', 'item_demanda']

class IndicacaoAdmin(admin.ModelAdmin):
    list_display = ['myname', 'email', 'myfone', 'organizacao', 'email_org', 'tel_org', 'acao_solidaria', 'data', 'is_new']
    list_filter = ['data', 'is_new']
    search_fields = ['myname', 'organizacao']

admin.site.register(Indicacao, IndicacaoAdmin)
admin.site.register(TermoUso, TermoUsoAdmin)
admin.site.register(AceiteTermo, AceiteTermoAdmin)
admin.site.register(TipoTerritorio, TipoTerritorioAdmin)
admin.site.register(Localidade, LocalidadeAdmin)
admin.site.register(Coordenada, CoordenadaAdmin)
admin.site.register(Organizacao, OrganizacaoAdmin)
admin.site.register(Representante, RepresentanteAdmin)
admin.site.register(AcaoSolidariaOferta, AcaoSolidariaOfertaAdmin)
admin.site.register(AcaoSolidariaDemanda, AcaoSolidariaDemandaAdmin)
admin.site.register(Categoria, CategoriaAdmin)
admin.site.register(Item, ItemAdmin)
admin.site.register(ItemAcaoOferta ,ItemAcaoOfertaAdmin)
admin.site.register(ItemAcaoDemanda, ItemAcaoDemandaAdmin)
admin.site.register(Encontro, EncontroAdmin)