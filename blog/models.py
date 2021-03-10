from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
from taggit.managers import TaggableManager


# Agregar custom manager
class PublishedManager(models.Manager):
    """
        Podemos definir custom managers para los modelos, en este caso obtener todos los Posts
        con el status = 'published'
    """

    def get_queryset(self):
        return super(PublishedManager, self).get_queryset().filter(status='published')


# Definir model Post
class Post(models.Model):
    """
        It's the data model for blog posts
    """
    STATUS_CHOICES = (
        ('draft', 'Draft'),
        ('published', 'Published'),
    )
    title = models.CharField(max_length=250)
    slug = models.SlugField(max_length=250, unique_for_date='publish')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blog_posts')
    body = models.TextField()
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')
    # Añadir tags al modelo
    tags = TaggableManager()

    # Campos custom manager
    # Manager por default
    objects = models.Manager()
    # Nuestro custom manager.
    published = PublishedManager()

    class Meta:
        ordering = ('-publish',)

    def __str__(self):
        """
        Str que devuelve el titulo
        :return: title
        """
        return self.title

    # Usar el URL de post detail para definir la construccion de una URL canonica
    # para los objectos post, para eso usaremos el metodo reverse(), que nos permite construir URLs
    # por su nombre y pasarle parametros opcionales
    def get_absolute_url(self):
        return reverse('blog:post_detail', args=[self.publish.year, self.publish.month, self.publish.day, self.slug])


class Comment(models.Model):
    """
        Creación del modelo de comentarios para los posts
    """
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    name = models.CharField(max_length=80)
    email = models.EmailField()
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ('created',)
    
    def __str__(self):
        return f'Comentado por {self.name} en {self.post}'
