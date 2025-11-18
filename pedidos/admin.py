from django.contrib import admin
from .models import Pedido, ItemPedido, Avaliacao

class ItemPedidoInline(admin.TabularInline):
    """
    Isto permite-nos ver e editar os Itens (produtos)
    DIRETAMENTE DENTRO do ecrã de Pedido.
    'extra=0' significa que não mostra linhas extra vazias.
    """
    model = ItemPedido
    extra = 0
    # readonly_fields = ('produto', 'quantidade', 'preco_unitario') # Descomente se quiser proibir edição

@admin.register(Pedido)
class PedidoAdmin(admin.ModelAdmin):
    """
    Configuração para o modelo Pedido no Admin.
    """
    list_display = ('id', 'comprador', 'data_hora_retirada', 'status', 'total')
    list_filter = ('status', 'data_hora_retirada')
    search_fields = ('comprador__username', 'id')
    
    # Aqui está a magia:
    # Mostra os 'ItemPedido' dentro da página de detalhe do 'Pedido'
    inlines = [ItemPedidoInline]

@admin.register(Avaliacao)
class AvaliacaoAdmin(admin.ModelAdmin):
    """
    Configuração para o modelo Avaliacao no Admin.
    """
    list_display = ('pedido', 'nota', 'data_criacao')
    list_filter = ('nota',)