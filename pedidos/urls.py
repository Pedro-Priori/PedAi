from django.urls import path
from . import views

app_name = 'pedidos'

urlpatterns = [
    path('meus-pedidos/', views.meus_pedidos, name= 'meus_pedidos')
]