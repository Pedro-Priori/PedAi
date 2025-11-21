from django.urls import path
from . import views

app_name = 'loja'

urlpatterns = [
    path('', views.home, name='home'),
    path('produto/<int:produto_id>/', views.detalhe_produto, name='detalhe'),
    
    
    path('minha-loja/', views.minha_loja, name='minha_loja'),
    
    
    path('minha-loja/adicionar/', views.adicionar_produto, name='adicionar_produto'),
    path('minha-loja/editar/<int:produto_id>/', views.editar_produto, name='editar_produto'),
]