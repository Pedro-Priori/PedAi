from django.db import models
from django.conf import settings # para referenciar o AUTH_USER_MODEL

class Produto(models.Model):
    """
    Representa um produto que um Vendedor pode listar no marketplace.
    O 'disponibilidade' é o nosso campo de Estoque.
    """
    
    # --- Relacionamentos ---
    vendedor = models.ForeignKey(
        settings.AUTH_USER_MODEL,  #  aponta para o nosso 'Usuario'
        on_delete=models.CASCADE,  # Se o vendedor for apagado, os seus produtos também são
        related_name="produtos",   # Permite aceder a Usuario.produtos
        # Garante que apenas utilizadores marcados como 'vendedor' podem ser ligados aqui
        limit_choices_to={'tipo_utilizador': 'vendedor'} 
    )
    
    # --- Campos ---
    nome = models.CharField(max_length=255)
    descricao = models.TextField(blank=True)
    preco = models.DecimalField(max_digits=10, decimal_places=2)
    
    # Lembra-te que instalámos o 'Pillow' para isto funcionar
    foto = models.ImageField(
        upload_to='fotos_produtos/', # Onde as fotos serão guardadas
        blank=True, 
        null=True
    )
    
    # Este é o campo de ESTOQUE
    disponibilidade = models.PositiveIntegerField(
        default=0,
        verbose_name="Estoque Disponível"
    )
    
    # Permite ao vendedor "desligar" um produto sem o apagar
    ativo = models.BooleanField(default=True) 

    def __str__(self):
        return f"{self.nome} - {self.vendedor.username}"

    class Meta:
        ordering = ['nome'] # Ordena os produtos por nome, por defeito