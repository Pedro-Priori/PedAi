from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Usuario

@admin.register(Usuario)
class UsuarioAdmin(UserAdmin):
    """
    Configuração para mostrar o nosso Usuario personalizado no Admin.
    Como estamos a usar o AbstractUser, podemos reutilizar o UserAdmin
    do Django, que já tem toda a segurança e campos prontos.
    """
    
    # Adiciona os nossos campos personalizados ('tipo_utilizador', 'local')
    # à lista de campos que o admin mostra.
    fieldsets = UserAdmin.fieldsets + (
        ('Campos Personalizados (PedAI)', {
            'fields': ('tipo_utilizador', 'local', 'telefone')
        }),
    )
    
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Novos Campos', {
            'fields': ('tipo_utilizador', 'local', 'telefone')
        }),
    )
    
    # Campos para mostrar na lista principal de utilizadores
    list_display = ['username', 'email', 'first_name', 'last_name', 'tipo_utilizador', 'is_staff']