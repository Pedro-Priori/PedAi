from django.shortcuts import render, redirect
from django.contrib.auth import login
from .forms import RegistoCompradorForm

def registro(request):
   
    if request.method == 'POST':
        form = RegistoCompradorForm(request.POST)
        
        
        if form.is_valid():
            user = form.save()
            login(request, user)
            
           
            if user.tipo_utilizador == 'vendedor':
                return redirect('loja:minha_loja')
            else:
                return redirect('loja:home')
    
    
    else:
        form = RegistoCompradorForm()
    
    
    return render(request, 'registration/registro.html', {'form': form})