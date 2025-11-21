import qrcode
from django.contrib.auth.decorators import login_required
from io import BytesIO
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render
from .models import Pedido

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