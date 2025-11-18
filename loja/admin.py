from django.contrib import admin
from .models import Produto

@admin.register(Produto)
class ProdutoAdmin(admin.ModelAdmin):
    """
    Configuração para o modelo Produto no Admin.
    """
    # Campos que aparecem na lista de produtos
    list_display = ('nome', 'vendedor', 'preco', 'disponibilidade', 'ativo')
    
    # Filtros que aparecem na barra lateral
    list_filter = ('vendedor', 'ativo')
    
    # Campos de pesquisa
    search_fields = ('nome', 'vendedor__username') # Permite procurar pelo nome do produto ou username do vendedor