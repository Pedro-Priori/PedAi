from django import forms 
from .models import Avaliacao

class AvaliacaoForm(forms.ModelForm):
    class Meta: 
        model = Avaliacao
        fields = ['nota', 'comentario']
        
        widgets = {
            'nota': forms.RadioSelect(choices=[
                (1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5')
            ]), 
            'comentario' : forms.Textarea(attrs={
                'class': 'forms-control',
                'rows' : 3,
                'placeholder': 'Nos diga o que acho?'
            })
        }

