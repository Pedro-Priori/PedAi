from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Produto
from pedidos.models import Pedido, ItemPedido
from .forms import ProdutoForm


def home(request):
    produtos = Produto.objects.filter(ativo=True, disponibilidade__gt=0).order_by('nome')
    return render(request, 'loja/home.html', {'produtos': produtos})

@login_required
def minha_loja(request):
    
    if request.user.tipo_utilizador != 'vendedor':
        messages.warning(request, "Você não tem permissão de vendedor.")
        return redirect('loja:home')
    
    produtos = Produto.objects.filter(vendedor=request.user)
    return render(request, 'loja/minha_loja.html', {'produtos': produtos})

@login_required
def adicionar_produto(request):
    
    if request.user.tipo_utilizador != 'vendedor':
        return redirect('loja:home')
    
    if request.method == 'POST':
        form = ProdutoForm(request.POST, request.FILES)
        
        if form.is_valid():
            produto = form.save(commit= False)
            produto.vendedor = request.user
            produto.save()
            
            messages.success(request, "Produto adicionado com Sucesso!")
            return redirect('loja:minha_loja')
        
    else:
        form = ProdutoForm()
            
    return render(request, 'loja/adicionar_produto.html', {'form': form})

@login_required
def painel_vendas(request):
    if request.user.tipo_utilizador != 'vendedor':
        return redirect('loja:home')
    
    itens_vendidos = ItemPedido.objects.filter(produto__vendedor=request.user).order_by('-pedido__data_criacao')
    
    return render(request, 'loja/painel_vendas.html', {'itens': itens_vendidos})

@login_required
def atualizar_pedido(request, pedido_id, novo_status):
    
    pedido = get_object_or_404(Pedido, id=pedido_id, itens__produto__vendedor=request.user)
    pedido.status = novo_status
    pedido.save()
    messages.success(request, f"Status atualizado para {novo_status}")
    return redirect('loja:painel_vendas')

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
def editar_produto(request, produto_id):
    produto = get_object_or_404(Produto, id=produto_id, vendedor=request.user)

    if request.method == 'POST':
        form = ProdutoForm(request.POST, request.FILES, instance=produto)
        if form.is_valid():
            form.save()
            messages.success(request, "Produto atualizado!")
            return redirect('loja:minha_loja')
    else:
        form = ProdutoForm(instance=produto)

    return render(request, 'loja/editar_produto.html', {'form': form, 'produto': produto})

@login_required
def excluir_produto(request, produto_id):
   
    produto = get_object_or_404(Produto, id=produto_id, vendedor=request.user)

    if request.method == 'POST':
        
        produto.delete()
        messages.success(request, "Produto removido com sucesso!")
        return redirect('loja:minha_loja')

    return render(request, 'loja/confirmar_exclusao.html', {'produto': produto})

@login_required
def cancelar_pedido(request, pedido_id):
    
    pedido = get_object_or_404(Pedido, id=pedido_id, itens__produto__vendedor=request.user)
    
    if pedido.status == 'cancelado':
        messages.warning(request, "Este pedido já foi cancelado.")
        return redirect('loja:painel_vendas')

    
    for item in pedido.itens.all():
        produto = item.produto
        produto.disponibilidade += item.quantidade
        produto.save()
    
    pedido.status = 'cancelado'
    pedido.save()
    
    messages.error(request, f"Pedido #{pedido.id} cancelado e estoque devolvido.")
    return redirect('loja:painel_vendas')