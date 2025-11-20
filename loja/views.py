from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Produto
from pedidos.models import Pedido, ItemPedido

def home(request):
    produtos = Produto.objects.filter(ativo=True, disponibilidade__gt=0).order_by('nome')
    return render(request, 'loja/home.html', {'produtos': produtos})


@login_required
def detalhe_produto(request, produto_id):
    produto = get_object_or_404(Produto, pk=produto_id)

    if request.method == 'POST':
        quantidade = int(request.POST.get('quantidade'))
        data_retirada = request.POST.get('data_retirada')
        
        if quantidade > produto.disponibilidade:
            messages.error(request, "Estoque insuficiente!")
            return redirect('loja:detalhe', produto_id=produto.id)
            
        if request.user.tipo_utilizador != 'comprador':
            messages.error(request, "Apenas Compradores podem fazer pedidos.")
            return redirect('loja:detalhe', produto_id=produto.id)

        pedido = Pedido.objects.create(
            comprador=request.user,
            status='pendente',
            data_hora_retirada=data_retirada,
            total=0
        )
        
        item = ItemPedido.objects.create(
            pedido=pedido,
            produto=produto,
            quantidade=quantidade,
            preco_unitario=produto.preco
        )
        
        pedido.total = item.preco_unitario * item.quantidade
        pedido.save()
        
        messages.success(request, "Pedido realizado com sucesso!")
        return redirect('pedidos:meus_pedidos')
    

    return render(request, 'loja/detalhe.html', {'produto': produto})

@login_required
def minha_loja(request):
    
    if request.user.tipo_utilizador != 'vendedor':
        return redirect('loja:home')

    produtos = Produto.objects.filter(vendedor=request.user)
    
    return render(request, 'loja/minha_loja.html', {'produtos': produtos})