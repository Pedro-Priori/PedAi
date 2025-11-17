from django.contrib.auth.models import AbstractUser
from django.db import models

class Usuario(AbstractUser):
    """
    Modelo de Utilizador personalizado que substitui o User padrão.
    Inclui os tipos de utilizador (comprador ou vendedor) e o bairro,
    essencial para o dashboard.
    """
    
    # --- Tipos de Utilizador ---
    class Tipo(models.TextChoices):
        COMPRADOR = 'comprador', 'Comprador'
        VENDEDOR = 'vendedor', 'Vendedor'

    tipo_utilizador = models.CharField(
        max_length=10,
        choices=Tipo.choices,
        default=Tipo.COMPRADOR, # Por defeito, quem se regista é comprador
        verbose_name="Tipo de Utilizador"
    )
    
    telefone = models.CharField(max_length=20, blank=True, null=True)
    
    # O local 
    local = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        # Mostra o username e o tipo entre parênteses
        return f"{self.username} ({self.get_tipo_utilizador_display()})"