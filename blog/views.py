from django.shortcuts import render, get_object_or_404
from .models import Post, Comment
# Paginator
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
# ListView class-based view
from django.views.generic import ListView
# Importar EmailPostForm, Commentform y SearchForm
from .forms import EmailPostForm, CommentForm, SearchForm
# Importar send_mail
from django.core.mail import send_mail
# Importar tags
from taggit.models import Tag
# Importar Count
from django.db.models import Count
# Importar Search
from django.contrib.postgres.search import SearchVector, SearchQuery, SearchRank


def post_list(request, tag_slug=None):
    '''
    Crear una vista para mostrar la lista total de los Posts,
    le pasamos el tag_slug de manera opcional por la URL
    '''
    object_list = Post.published.all()

    # Añadir tag
    tag = None

    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        object_list = object_list.filter(tags__in=[tag])

    paginator = Paginator(object_list, 1) # 3 post por pagina
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer deliver the first page
        posts = paginator.page(1)
    except EmptyPage:
        # If page is out of range deliver last page of results
        posts = paginator.page(paginator.num_pages)

    return render(request, 'blog/post/list.html', {'page': page,'posts': posts, 'tag': tag})


def post_detail(request, year, month, day, post):
    """
    Crear una vista para mostrar el detalle de solo un Post
    """
    post = get_object_or_404(Post, slug=post,
                             status='published',
                             publish__year=year,
                             publish__month=month,
                             publish__day=day)
    
    # Lista de comentarios activos para este post
    comments = post.comments.filter(active=True)

    new_comment = None

    if request.method == 'POST':
        # Un comentario fue publicado
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            # Crear objeto Comment pero sin guardarlo en la bd todavia
            new_comment = comment_form.save(commit=False)
            # Asignar el post actual al comentario
            new_comment.post = post
            # Guardar el comentario en la bd
            new_comment.save()
    else:
        comment_form = CommentForm()
    
    # Lista de posts similares (importante)
    post_tags_ids = post.tags.values_list('id', flat=True)
    similar_posts = Post.published.filter(tags__in=post_tags_ids).exclude(id=post.id)
    similar_posts = similar_posts.annotate(same_tags=Count('tags')).order_by('-same_tags', '-publish') [:4]
    
    return render(request, 'blog/post/detail.html', {'post': post,
                                                    'comments':comments, 
                                                    'new_comment':new_comment,
                                                    'comment_form': comment_form,
                                                    'similar_posts': similar_posts})


def post_share(request, post_id):
    """
    Crear una nueva vista que maneje el formulario y enviarlos a un email
    cuando es realizado correctamente.
    """
    # Obtener post por su id
    post = get_object_or_404(Post, id=post_id, status='published')
    sent = False

    if request.method == 'POST':
        # Form fue enviado
        form = EmailPostForm(request.POST)
        if form.is_valid():
            # Campos de formulario al pasar la validación
            cd = form.cleaned_data
            # ... enviar email
            post_url = request.build_absolute_uri(post.get_absolute_url())
            subject = f"{cd['name']} te recomienda leer " f"{post.title}"
            message = f"Leer {post.title} en {post_url}\n\n" f"Comentario de {cd['name']}: {cd['comments']}"
            send_mail(subject, message, 'loquendoturbina@gmail.com', [cd['to']])
            sent = True    
                    
    else:
        form = EmailPostForm()
    return render(request, 'blog/post/share.html', {'post':post, 'form':form, 'sent':sent})


def post_search(request):
    """
    Crear funcion de busqueda de posts llamando el form SearchForm
    Cuando el formulario es emitido,mandas el formulario usando el metodo GET
    atraves del POST. Cuando el formulario es emiido se instancia con los datos enviados por GET
    y verifica que los datos sean validos, si el formulario es valido puedes buscar los post
    publicados con la instancia custom SearchVector construida con los campos titulo y body  

    Se aplican diferentes weights a la busqueda construida por el title y body
    los weights defaults son D, C, B y A y se refieren a numeros 0.1, 0.2, 0.4 y 1.0 respectivamente
    Puedes aplicar un weight de 1.0 para el title y weight de 04 al body
    los resultados de title van a prevalecer sobre el contenido compatible con el body
    Se filtra el resultado para mostrar solo los que tengan el rank mas alto de 0.3
    """
    form = SearchForm()
    query = None
    results = []
    if 'query' in request.GET:
        form = SearchForm(request.GET)
        if form.is_valid():
            query = form.cleaned_data['query']
            search_vector = SearchVector('title', weight='A') + SearchVector('body', weight='B')
            search_query = SearchQuery(query)
            results = Post.published.annotate(
                            search=search_vector,
                            rank=SearchRank(search_vector, search_query)
                            ).filter(rank__gte=0.3).order_by('-rank')
            """results = Post.published.annotate(
                            search=search_vector,
                            rank=SearchRank(search_vector, search_query)
                            ).filter(search=search_query).order_by('-rank')"""
            #results = Post.published.annotate(search=SearchVector('title', 'body'),).filter(search=query)
    return render(request, 'blog/post/search.html',
                            {'form': form,
                            'query': query,
                            'results': results})






"""
*********************************
***** VISTAS OPCIONALES *********
*********************************
"""


"""
class PostListView(ListView):
    '''
    This class-based view is analogous to the previous post_list view.
    Use a specific Queryset instead of retrieving all objects.
    Instead of defining a queryset attribute, you could have specified model = Post
    and Django would have build the generif Post.objects.all() Queryset

    Use the context variable posts for query results. The default variable is
    object_list if you don't spicify any contex_object_name.

    Paginate the result, displaying 'n' objects per page.

    Use a custom template to render the page. If you don't set a default template,
    ListView will use blog/post_list.html
    '''
    queryset = Post.published.all()
    context_object_name = 'posts'
    paginate_by = 1
    template_name = 'blog/post/list.html'
"""