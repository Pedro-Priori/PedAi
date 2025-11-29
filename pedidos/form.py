from django import forms 
from .models import Avaliacao

class AvaliacaoForm(forms.ModelForm):
    class Meta: 
        model = Avaliacao
        fields = ['nota', 'comentario']
        
        widgets = {
            'Nota' : forms.NumberInput(attrs={
                'class' : 'form-control',
                'min' : '1',
                'max' : '5',
                'placeholder' : 'De 1 a 5'
            }), 
            'comentario' : forms.Textarea(attrs={
                'class': 'forms-control',
                'rows' : 3,
                'placeholder': 'Nos diga o que acho?'
            })
        }
