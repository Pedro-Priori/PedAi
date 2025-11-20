from django.db import models
from django.conf import settings
from loja.models import Produto
from django.core.validators import MinValueValidator, MaxValueValidator
import uuid 



class Pedido(models.Model):
    """
    Representa o pedido (reserva) feito por um Comprador.
    """
    
    class Status(models.TextChoices):
        PENDENTE = 'pendente', 'Pendente'
        CONFIRMADO = 'confirmado', 'Confirmado'
        CONCLUIDO = 'concluido', 'Concluído'
        CANCELADO = 'cancelado', 'Cancelado'

    
    comprador = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name="pedidos",
        limit_choices_to={'tipo_utilizador': 'comprador'}
    )
    
    
    produtos = models.ManyToManyField(Produto, through='ItemPedido')


    status = models.CharField(
        max_length=15, 
        choices=Status.choices, 
        default=Status.PENDENTE
    )
    
    data_hora_retirada = models.DateTimeField(
        verbose_name="Horário Definido para Retirada"
    )
    

    qr_code_id = models.UUIDField(
        default=uuid.uuid4, 
        editable=False, 
        unique=True
    )
    
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    data_criacao = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Pedido {self.id} de {self.comprador.username} ({self.get_status_display()})"


class ItemPedido(models.Model):
    """
    Este é o modelo "ponte" (through model) que liga um Pedido a um Produto.
    É aqui que guardamos a quantidade e implementamos a lógica de ESTOQUE.
    """
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE, related_name="itens")
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE, related_name="itens_pedido")
    quantidade = models.PositiveIntegerField(default=1)
    

    preco_unitario = models.DecimalField(max_digits=10, decimal_places=2) 

    def __str__(self):
        return f"{self.quantidade}x {self.produto.nome} @ {self.preco_unitario}"

  
    def save(self, *args, **kwargs):
    
        if not self.pk: 
            if self.produto.disponibilidade < self.quantidade:
                
                raise ValueError(f"Estoque insuficiente para {self.produto.nome}.")
            
        
            self.produto.disponibilidade -= self.quantidade
            self.produto.save()
        
        
        self.preco_unitario = self.produto.preco 
        
        super().save(*args, **kwargs) 

    def delete(self, *args, **kwargs):

        self.produto.disponibilidade += self.quantidade
        self.produto.save()
        super().delete(*args, **kwargs)


class Avaliacao(models.Model):
    """
    Avaliação ligada a um Pedido.
    Um pedido só pode ter uma avaliação (One-to-One).
    """
    pedido = models.OneToOneField(
        Pedido,
        on_delete=models.CASCADE, 
        related_name="avaliacao"  
    )
    
    nota = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(10)],
    )
    comentario = models.TextField(blank=True, null=True)
    data_criacao = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Avaliação ({self.nota} estrelas) para Pedido {self.pedido.id}"
