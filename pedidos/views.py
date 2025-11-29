import qrcode
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from io import BytesIO
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render, redirect
from .models import Pedido, Avaliacao
from .form import AvaliacaoForm

@login_required
def meus_pedidos(request): 
    pedidos = Pedido.objects.filter(comprador=request.user).order_by('-data_criacao')
    return render(request, 'pedidos/meus_pedidos.html', {'pedidos':pedidos})
def gerar_qrcode(request, pedido_id):
    pedido = get_object_or_404(Pedido, pk=pedido_id)
    
    if pedido.comprador != request.user:
        return HttpResponse("Acesso Negado", status = 403)
    
    conteudo_qr = f"PEDIDO-{pedido.qr_code_id}"
    img = qrcode.make(conteudo_qr)
    
    buffer = BytesIO()
    img.save(buffer, format= "PNG")
    
    return HttpResponse(buffer.getvalue(), content_type = "image/png")

@login_required
def Avaliar_pedido(request, pedido_id): 
    
    pedido = get_object_or_404(Pedido, id = pedido_id, comprador = request.user)
    
    if pedido.status != 'concluido' : 
        messages.error(request, "Você só poder avaliar pedios concluidos e entregues . ")
        return redirect('pedidos:meus_pedidos')
    
    if hasattr(pedido, 'avaliacao'): 
        messages.warning(request, "Você ja avaliou este pedido")
        return redirect('pedidos:meus_pedidos')
    
    if request.method == 'POST':
        form = AvaliacaoForm(request.POST)
        if form.is_valid():
            avaliacao = form.save(commit=False)
            avaliacao.pedido = pedido
            avaliacao.save()
            
            messages.success(request, "Obrigado pela sua Avaliação")
            return redirect('pedidos:meus_pedidos')
    
    else: 
        form = AvaliacaoForm()
        
    return render(request, 'pedidos/avaliar_pedido.html', {'form': form, 'pedido': pedido} )