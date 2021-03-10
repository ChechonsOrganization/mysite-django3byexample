""" Crear forms.py para crear formularios valga la redundancia."""
# Importar forms
from django import forms
# Importar modelo Comment
from .models import Comment


class EmailPostForm(forms.Form):
    """
    Clase Form para construir un formulario estandar (no estan enlazados a ningun modelo)
    Construcción de formulario para compartir posts
    """
    name = forms.CharField(max_length=25)
    email = forms.EmailField()
    to = forms.EmailField()
    comments = forms.CharField(required=False, widget=forms.Textarea)


class CommentForm(forms.ModelForm):
    """
    Clase para construir el formulario para los comentarios
    necesitaremos el forms.ModelForm para construir el form
    dinamicamente para el modelo Comment.
    """

    class Meta:
        model = Comment
        fields = ('name', 'email', 'body')


class SearchForm(forms.Form):
    query = forms.CharField()