import uuid

from django.db import models
from django_min_custom_user.models import MinAbstractUser


class User(MinAbstractUser):
    pass


class UrlRedirect(models.Model):
    destino = models.URLField(verbose_name='Destino URL')
    slug = models.SlugField(verbose_name='Slug', unique=True)
    criado_em = models.DateTimeField(auto_now_add=True)  # Data de criação
    atualizado_em = models.DateTimeField(auto_now=True)  # Data de atualização

    def save(self, *args, **kwargs):
        if not self.slug:  # Gera um slug único somente se estiver vazio
            self.slug = uuid.uuid4().hex[:8]  # Cria um slug curto e único
        super().save(*args, **kwargs)

    def __str__(self):
        return f'UrlRedirect para {self.destino}'


class UrlLog(models.Model):
    criado_em = models.DateTimeField(auto_now_add=True)
    origem = models.URLField(max_length=512, null=True, blank=True)
    user_agent = models.CharField(max_length=512, null=True, blank=True)
    host = models.CharField(max_length=512, null=True, blank=True)
    ip = models.GenericIPAddressField(null=True, blank=True)
    url_redirect = models.ForeignKey(UrlRedirect, models.DO_NOTHING, related_name='logs')

    def __str__(self):
        iso = self.criado_em.isoformat()
        return f'{iso}: {self.origem}'
