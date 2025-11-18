# Em loja/views.py
from django.shortcuts import render
from .models import Produto # Importa o nosso modelo Produto

def home(request):
    """
    Esta é a View (função de lógica) para a nossa página inicial.
    """
    
  
    produtos_disponiveis = Produto.objects.filter(
        ativo=True, 
        disponibilidade__gt=0  # __gt significa "greater than" (maior que)
    ).order_by('nome') # Ordena por nome
    

    contexto = {
        'produtos': produtos_disponiveis,
    }
    

    return render(request, 'loja/home.html', contexto)