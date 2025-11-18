# Em loja/urls.py
from django.urls import path
from . import views  # Importa as nossas views (o ficheiro views.py)

# app_name define um "espaço de nomes" para os URLs
# (Boa prática para projetos grandes)
app_name = 'loja'

urlpatterns = [
    # Quando o caminho for "vazio" (a raiz da app),
    # executa a função 'home' que está em views.py
    # 'name="home"' é um apelido para este URL.
    path('', views.home, name='home'),
]