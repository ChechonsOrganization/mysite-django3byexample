""" 
Custom template tags
"""
from django import template
from django.db.models import Count
from ..models import Post

#Importes de Custom filter
from django.utils.safestring import mark_safe
import markdown


register = template.Library()


@register.simple_tag
def total_posts():
    """ 
    Crear un simple tag que retorne el 
    numero de posts publicados 
    """
    return Post.published.count()


@register.inclusion_tag('blog/post/latest_posts.html')
def show_latest_posts(count=5):
    """
    Crear un inclusion tag para mostrar los ultimos
    5 post publicados en un sidebar reutilizable por vistas
    """
    latest_posts = Post.published.order_by('-publish') [:count]
    return {'latest_posts': latest_posts}


@register.simple_tag
def get_most_commented_posts(count=5):
    """
    Crear un simple tag que retorne los posts mas populares,
    en este caso seran los que mas comentarios tengan.
    """
    return Post.published.annotate(total_comments=Count('comments')).order_by('-total_comments') [:count]
    

@register.filter(name='markdown')
def markdown_format(text):
    """
    Crear un custom filter para convertir el texto 
    simple a HTML usando el markdown syntax
    """
    return mark_safe(markdown.markdown(text))