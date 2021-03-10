# Agregando Patrones URL a las vistas
from django.urls import path
from . import views
# Feed
from .feeds import LatestPostFeed

app_name = 'blog'

urlpatterns = [
    # Vistas de Post
    
    # Path para llamar la vista de todos los Posts
    path('', views.post_list, name='post_list'),

    # Path para listar los post por tag
    path('tag/<slug:tag_slug>/', views.post_list, name='post_list_by_tag'),

    # Reemplazar Path post_list por PostListView (Comentado para activar el primero)
    # path('', views.PostListView.as_view(), name='post_list'),
    
    # Path para llamar la vista de detalle de un Post
    path('<int:year>/<int:month>/<int:day>/<slug:post>/', views.post_detail, name='post_detail'),
    
    # Path de la vista post_share para compartir posts
    path('<int:post_id>/share/', views.post_share, name='post_share'),

    # Path del feeds.py
    path('feed/', LatestPostFeed(), name='post_feed'),

    # Path para la busqueda de posts
    path('search/', views.post_search, name='post_search'),
]