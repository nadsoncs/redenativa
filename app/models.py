from django.db import models
from django.contrib.auth.models import User
from .managers import OrgManager
###########################################
########
STATES_CHOICES = (
    ('AC', 'Acre'),
    ('AL', 'Alagoas'),
    ('AP', 'Amapá'),
    ('AM', 'Amazonas'),
    ('BA', 'Bahia'),
    ('CE', 'Ceará'),
    ('DF', 'Distrito Federal'),
    ('ES', 'Espírito Santo'),
    ('GO', 'Goiás'),
    ('MA', 'Maranhão'),
    ('MT', 'Mato Grosso'),
    ('MS', 'Mato Grosso do Sul'),
    ('MG', 'Minas Gerais'),
    ('PA', 'Pará'),
    ('PB', 'Paraíba'),
    ('PR', 'Paraná'),
    ('PE', 'Pernambuco'),
    ('PI', 'Piauí'),
    ('RJ', 'Rio de Janeiro'),
    ('RN', 'Rio Grande do Norte'),
    ('RS', 'Rio Grande do Sul'),
    ('RO', 'Rondônia'),
    ('RR', 'Roraima'),
    ('SC', 'Santa Catarina'),
    ('SP', 'São Paulo'),
    ('SE', 'Sergipe'),
    ('TO', 'Tocantins'),
)

ORG_CHOICES = (
    ('A', 'Associação'),
    ('C', 'Comunidade'),
    ('E', 'Empresa'),
    ('I', 'Instituição'),
    ('O', 'Outro'),
)
ITEM_CHOICES = (
    ('m', 'Metro'),
    ('lt', 'Litro'),
    ('kg', 'Quilo'),
    ('un', 'Unidade'),
    ('hr', 'Hora'),
)
IMAGE_FOLDER = 'images'
###########################################

# Create your models here.


class TermoUso(models.Model):
    arquivo = models.FileField(upload_to= "", default="")
    data = models.DateField(auto_now = True)
    is_active = models.BooleanField(default=True, verbose_name='ativo?')
    
    def chage_view(self):
        return self.arquivo

    class Meta:
        verbose_name = 'Termo de uso'
        verbose_name_plural = 'Termos de uso'
    
    def __str__(self):
        return "%s" % (self.data)

class AceiteTermo(models.Model):
    termo = models.ForeignKey(TermoUso, on_delete=models.PROTECT)
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    class Meta:
        unique_together = ('termo', 'user')

    @staticmethod    
    def has_read_permission(request):
        return True

    def has_object_read_permission(self, request):
        return True
   
    #def has_object_create_permission(self, request):
    def has_object_write_permission(self, request):
        return request.user == self.user

class TipoTerritorio(models.Model):
    name = models.CharField(max_length=100, verbose_name='nome')
    is_active = models.BooleanField(default=False, verbose_name='ativo?')
    is_new = models.BooleanField(default=True, verbose_name='novo?')
    def __str__(self):
        return self.name
    class Meta:
        verbose_name = 'tipo de território'
        verbose_name_plural = 'tipos de território'

class Localidade(models.Model):
    estado = models.CharField(max_length=2, choices=STATES_CHOICES)
    cidade = models.CharField(max_length=45, verbose_name='cidade')
    bairro = models.CharField(max_length=45, verbose_name='bairro')
    cep = models.CharField(max_length=8, blank=True,verbose_name='CEP')
    tipo = models.ForeignKey(TipoTerritorio, on_delete=models.PROTECT)
    def __str__(self):
        return "%s-%s, %s" % (self.cidade, self.estado, self.bairro)

class Coordenada(models.Model):
    localidade = models.OneToOneField(Localidade, on_delete=models.CASCADE)
    latitude = models.FloatField()
    longitude = models.FloatField()
    raio = models.FloatField()

class Organizacao(models.Model):
    name = models.CharField(max_length=100, verbose_name='nome')
    email = models.EmailField(max_length=128, verbose_name='email')
    tipo = models.CharField(max_length=1, choices=ORG_CHOICES)
    tel = models.CharField(max_length=15, verbose_name='telefone')
    is_active = models.BooleanField(default=True, verbose_name='ativo?')
    localidade = models.ForeignKey(Localidade, on_delete=models.PROTECT)
    logo = models.ImageField(upload_to=IMAGE_FOLDER, height_field=None, width_field=None, blank=True)
    
    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "organização"
        verbose_name_plural = "organizações"

class Representante(models.Model):
    cargo = models.CharField(max_length=100, verbose_name='cargo')
    user = models.OneToOneField(User, on_delete=models.PROTECT)
    organizacao = models.ForeignKey(Organizacao, on_delete=models.PROTECT)

class Categoria(models.Model):
    name = models.CharField(max_length=100, verbose_name='nome')
    is_active = models.BooleanField(default=False, verbose_name='ativo?')
    is_new = models.BooleanField(default=True, verbose_name='novo?')
    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "categoria"
        verbose_name_plural = "categorias"

class AcaoSolidariaOferta(models.Model):
    name = models.CharField(max_length=100, verbose_name='nome')
    descricao = models.TextField()
    is_covid = models.BooleanField(default=True, verbose_name='covid-19?')
    data = models.DateField(auto_now = True)
    validade = models.DateField(auto_now = False , auto_now_add = False, blank=True)
    organizacao = models.ForeignKey(Organizacao, on_delete=models.PROTECT)
    localidade = models.OneToOneField(Localidade, on_delete=models.CASCADE)
    categoria = models.ForeignKey(Categoria, on_delete=models.PROTECT)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "ação solidaria - oferta"
        verbose_name_plural = "ações solidarias - oferta"

class AcaoSolidariaDemanda(models.Model):
    name = models.CharField(max_length=100, verbose_name='nome')
    descricao = models.TextField()
    is_covid = models.BooleanField(default=True, verbose_name='covid-19?')
    num_familias = models.PositiveSmallIntegerField()
    data = models.DateField(auto_now = True)
    validade = models.DateField(auto_now = False , auto_now_add = False, blank=True)
    organizacao = models.ForeignKey(Organizacao, on_delete=models.PROTECT)
    categoria = models.ForeignKey(Categoria, on_delete=models.PROTECT)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "ação solidaria - demanda"
        verbose_name_plural = "ações solidarias - demanda"

class Item(models.Model):
    name = models.CharField(max_length=100, verbose_name='nome')
    un_medida = models.CharField(max_length=2, choices=ITEM_CHOICES, blank=True)
    categoria = models.ManyToManyField(Categoria)

    def __str__(self):
        return self.name +" - "+ self.un_medida

    class Meta:
        verbose_name = "item"
        verbose_name_plural = "itens"

class ItemAcaoOferta(models.Model):
    a_s_oferta = models.ForeignKey(AcaoSolidariaOferta, related_name='itens_acao', on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.PROTECT)
    qtd_inicial = models.PositiveSmallIntegerField()
    saldo = models.PositiveSmallIntegerField()
    data = models.DateField(auto_now = True)

    def __str__(self):
        return "%s | %s" % (self.a_s_oferta.name, self.item)
    
    class Meta:
        verbose_name = "item da ação solidaria - oferta"
        verbose_name_plural = "itens da ação solidaria - oferta"

class ItemAcaoDemanda(models.Model):
    a_s_demanda = models.ForeignKey(AcaoSolidariaDemanda, related_name='itens_acao', on_delete=models.PROTECT)
    item = models.ForeignKey(Item, on_delete=models.PROTECT)
    qtd_inicial = models.PositiveSmallIntegerField()
    saldo = models.PositiveSmallIntegerField()
    data = models.DateField(auto_now = True)

    def __str__(self):
        return "%s | %s" % (self.a_s_demanda, self.item)
    
    class Meta:
        verbose_name = "item da ação solidaria - demanda"
        verbose_name_plural = "itens da ação solidaria - demanda"

class Encontro(models.Model):
    item_oferta = models.ForeignKey(ItemAcaoOferta, on_delete=models.PROTECT)
    item_demanda = models.ForeignKey(ItemAcaoDemanda, on_delete=models.PROTECT)
    is_total = models.BooleanField(default=True, verbose_name='Totalmente?')
    data = models.DateField(auto_now = True)

    class Meta:
        verbose_name = "encontro"

    def __str__(self):
        return "%s | %s" % (self.item_oferta, self.item_demanda)

class Indicacao(models.Model):
    #dados de quem indica
    myname = models.CharField(max_length=100, verbose_name='indicado por')
    email = models.EmailField(max_length=128, verbose_name='email')
    myfone = models.CharField(max_length=15, verbose_name='telefone pessoal')
    #dados de empresa indicada
    organizacao = models.CharField(max_length=100, verbose_name='organização')
    email_org = models.EmailField(max_length=128, verbose_name='email organização', blank=True)
    tel_org = models.CharField(max_length=15, verbose_name='telefone organização', blank=True)
    #dados da ação solidária
    acao_solidaria = models.CharField(max_length=100, verbose_name='ação solidaria')
    descrição = models.TextField()
    data = models.DateField(auto_now = True)
    is_new = models.BooleanField(default=True, verbose_name='novo?')

    class Meta:
        verbose_name = "indicação"
        verbose_name_plural = "indicações"

        