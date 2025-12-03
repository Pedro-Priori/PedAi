from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Usuario

class RegistoCompradorForm(UserCreationForm):
    class Meta:
        model = Usuario
        
        fields = ('username', 'email', 'first_name', 'local', 'tipo_utilizador')
        
        widgets = {
            
            'tipo_utilizador' : forms.Select(attrs={'class':'form-select'}),
            'local' : forms.TextInput(attrs={'class':'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class':'form-control'}),
            'username' : forms.TextInput(attrs={'class':'form-control'})       
         
         }
        
        labels = {
            'tipo_utilizador':'Sou :',
            'local': 'Meu local é '
        }
        