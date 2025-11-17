from django.db import models
from django.conf import settings
from loja.models import Produto # Importamos o Produto da app 'loja'
from django.core.validators import MinValueValidator, MaxValueValidator
import uuid # Para gerar IDs únicos para os pedidos



class Pedido(models.Model):
    """
    Representa o pedido (reserva) feito por um Comprador.
    """
    
    class Status(models.TextChoices):
        PENDENTE = 'pendente', 'Pendente'
        CONFIRMADO = 'confirmado', 'Confirmado'
        CONCLUIDO = 'concluido', 'Concluído'
        CANCELADO = 'cancelado', 'Cancelado'

    # --- Relacionamentos ---
    comprador = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL, # Se o comprador for apagado, o pedido fica no histórico
        null=True,
        related_name="pedidos",
        limit_choices_to={'tipo_utilizador': 'comprador'}
    )
    
    # Um pedido pode ter vários produtos.
    # Usamos um modelo 'through' (ItemPedido) para especificar a QUANTIDADE.
    produtos = models.ManyToManyField(Produto, through='ItemPedido')

    # --- Campos ---
    status = models.CharField(
        max_length=15, 
        choices=Status.choices, 
        default=Status.PENDENTE
    )
    
    data_hora_retirada = models.DateTimeField(
        verbose_name="Horário Definido para Retirada"
    )
    
    # O ID que será usado para gerar o QR Code
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
    
    # Guarda o preço no momento da compra
    preco_unitario = models.DecimalField(max_digits=10, decimal_places=2) 

    def __str__(self):
        return f"{self.quantidade}x {self.produto.nome} @ {self.preco_unitario}"

    # ---------------------------------------------------------------------
    # AQUI ESTÁ A TUA LÓGICA DE ESTOQUE AUTOMÁTICO!
    # ---------------------------------------------------------------------
    def save(self, *args, **kwargs):
        # Esta função é chamada sempre que um ItemPedido é salvo.
        
        # Se o item está a ser criado (não tem 'id' ainda)
        if not self.pk: 
            if self.produto.disponibilidade < self.quantidade:
                # Se não houver estoque, não permitimos a criação
                raise ValueError(f"Estoque insuficiente para {self.produto.nome}.")
            
            # Diminui o estoque
            self.produto.disponibilidade -= self.quantidade
            self.produto.save()
        
        # Guarda o preço atual do produto no item
        self.preco_unitario = self.produto.preco 
        
        super().save(*args, **kwargs) # Salva o ItemPedido

    def delete(self, *args, **kwargs):
        # Se o item for removido do pedido (ou o pedido cancelado), 
        # devolvemos o estoque ao produto.
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
        on_delete=models.CASCADE, # Se o pedido for apagado, a avaliação também é
        related_name="avaliacao"  # Permite aceder a Pedido.avaliacao
    )
    
    nota = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)], # Nota de 1 a 5
    )
    comentario = models.TextField(blank=True, null=True)
    data_criacao = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Avaliação ({self.nota} estrelas) para Pedido {self.pedido.id}"
