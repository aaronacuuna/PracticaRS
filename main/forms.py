#encoding:utf-8
from django import forms
from main.models import Genero
   
class GeneroBusquedaForm(forms.Form):
    genero = forms.ModelChoiceField(queryset=Genero.objects.all(), label="Seleccione un género")
    
class UsuarioBusquedaForm(forms.Form):
    idUsuario = forms.CharField(label="Id de Usuario", widget=forms.TextInput, required=True)