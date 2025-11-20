from django.shortcuts import render, redirect
from django.contrib.auth import login
from .forms import RegistoCompradorForm

def registro(request):
    if request.method == 'POST':
        form = RegistoCompradorForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.tipo_utilizador = 'comprador' # Força ser Comprador
            user.save()
            login(request, user)
            return redirect('/')
    else:
        form = RegistoCompradorForm()
    return render(request, 'registration/registro.html', {'form': form})