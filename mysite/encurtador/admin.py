from django.contrib import admin
from django_min_custom_user.admin import MinUserAdmin

from mysite.encurtador.models import UrlLog, UrlRedirect, User


@admin.register(User)
class UserAdmin(MinUserAdmin):
    pass


@admin.register(UrlRedirect)
class UrlRedirectAdmin(admin.ModelAdmin):
    list_display = ('destino', 'slug', 'criado_em', 'atualizado_em')


@admin.register(UrlLog)
class UrlLogAdmin(admin.ModelAdmin):
    list_display = ('origem', 'criado_em', 'user_agent', 'host', 'ip', 'url_redirect')

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def has_add_permission(self, request):
        return False
