"""
Crear feeds para el blog
"""
from django.contrib.syndication.views import Feed
from django.template.defaultfilters import truncatewords
from django.urls import reverse_lazy
from .models import Post


class LatestPostFeed(Feed):
    """ 
    Clase para proveer a los usuarios las ultimas actualizaciones
    los usuarios podran subscribirse al feed usando el feed aggregator que es usado
    para leler feeds y obtener las nuevas notificaciones.
    """
    title = 'My Blog'
    link = reverse_lazy('blog:post_list')
    description = 'Nuevos post de mi blog'

    def items(self):
        return Post.published.all() [:5]

    def item_title(self, item):
        return item.title
    
    def item_description(self, item):
        return truncatewords(item.body, 30)