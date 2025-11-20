from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Pedido

@login_required
def meus_pedidos(request): 
    pedidos = Pedido.objects.filter(comprador=request.user).order_by('-data_criacao')
    return render(request, 'pedidos/meus_pedidos.html', {'pedidos':pedidos})