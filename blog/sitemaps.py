""" 
Añadir un sitemap al sitio
"""
from django.contrib.sitemaps import Sitemap
from .models import Post

class PostSitemap(Sitemap):
    """ 
    Crear un custom sitemap heredando por la clase sitemap
    del modulo sitemaps.

    los atributos changefreq y priority indican el cambio frecuente
    de las paginas de los post y sus relevancias en el sitio.
    (valor maximo 1).

    el metodo items() returna el QuerySet de objetos a incluir en el sitemap
    por default django llama al metodo get_absolute_url() en cada objeto para
    obtener su URL.  
    """

    changefreq = 'weekly'
    priority = 0.9

    def items(self):
        return Post.published.all()

    def lastmod(self, obj):
        return obj.updated