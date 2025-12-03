from django.urls import path
from . import views

app_name = 'loja'

urlpatterns = [
   # Rotas Públicas
    path('', views.home, name='home'),
    path('produto/<int:produto_id>/', views.detalhe_produto, name='detalhe'),
    
    # --- ÁREA DO VENDEDOR ---
    
    # 1. Painel Principal
    path('minha-loja/', views.minha_loja, name='minha_loja'),
    
    # 2. Adicionar Produto
    path('minha-loja/adicionar/', views.adicionar_produto, name='adicionar_produto'),
    
    # 3. Editar Produto (A ROTA QUE FALTAVA)
    path('minha-loja/editar/<int:produto_id>/', views.editar_produto, name='editar_produto'),

    # 4. Excluir Produto (Vamos precisar desta também)
    path('minha-loja/excluir/<int:produto_id>/', views.excluir_produto, name='excluir_produto'),

    # 5. Painel de Vendas
    path('minha-loja/vendas/', views.painel_vendas, name='painel_vendas'),
    
    # 6. Ações nos Pedidos
    path('pedido/atualizar/<int:pedido_id>/<str:novo_status>/', views.atualizar_pedido, name='atualizar_pedido'),
    path('pedido/cancelar/<int:pedido_id>/', views.cancelar_pedido, name='cancelar_pedido'),
]