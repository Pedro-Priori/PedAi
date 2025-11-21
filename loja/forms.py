from django import forms
from .models import Produto

class ProdutoForm(forms.ModelForm):
    class Meta: 
        model = Produto
        fields = ['nome','descricao','preco','disponibilidade','foto']
        
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-control'}),
            'descricao': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'preco': forms.NumberInput(attrs={'class': 'form-control'}),
            'disponibilidade': forms.NumberInput(attrs={'class': 'form-control'}),
            'foto': forms.FileInput(attrs={'class': 'form-control'}),
        }