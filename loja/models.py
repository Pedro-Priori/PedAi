from django.db import models
from django.conf import settings 

class Produto(models.Model):
    """
    Representa um produto que um Vendedor pode listar no marketplace.
    O 'disponibilidade' é o nosso campo de Estoque.
    """
    
    # --- Relacionamentos ---
    vendedor = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name="produtos",   
        
        limit_choices_to={'tipo_utilizador': 'vendedor'} 
    )
    
    # --- Campos ---
    nome = models.CharField(max_length=255)
    descricao = models.TextField(blank=True)
    preco = models.DecimalField(max_digits=10, decimal_places=2)
    
    
    foto = models.ImageField(
        upload_to='fotos_produtos/', 
        blank=True, 
        null=True
    )
    
    # Este é o campo de ESTOQUE
    disponibilidade = models.PositiveIntegerField(
        default=0,
        verbose_name="Estoque Disponível"
    )
    
    
    ativo = models.BooleanField(default=True) 

    def __str__(self):
        return f"{self.nome} - {self.vendedor.username}"

    class Meta:
        ordering = ['nome'] 