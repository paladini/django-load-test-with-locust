from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.core.paginator import Paginator
from django.db.models import F, Count
from django.views.decorators.cache import cache_page
from django.views.decorators.http import require_http_methods
from django.utils.decorators import method_decorator
from django.views.generic import ListView
from .models import Post, Category
import time
import random


def home(request):
    """View simples para homepage"""
    recent_posts = Post.objects.filter(published=True)[:5]
    categories = Category.objects.all()
    
    context = {
        'recent_posts': recent_posts,
        'categories': categories,
        'page_title': 'Blog Home'
    }
    return render(request, 'blog/home.html', context)


def post_list(request):
    """View com paginação - versão SEM otimização"""
    # Problema N+1 Queries
    # Para 10 posts, isso pode gerar 11 queries (1 para posts + 10 para autores)
    posts = Post.objects.filter(published=True).order_by('-created_at')
    
    # Adiciona um delay artificial para simular processamento
    time.sleep(0.1)
    
    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'page_title': 'Todos os Posts'
    }
    return render(request, 'blog/post_list.html', context)


def post_list_optimized(request):
    """View com paginação - versão OTIMIZADA"""
    
    # Problema N+1 Queries resolvido com select_related
    # Para 10 posts, isso gera apenas 2 queries (1 para posts + 1 para autores e categorias)
    posts = Post.objects.filter(published=True)\
                       .select_related('author', 'category')\
                       .order_by('-created_at')
    
    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'page_title': 'Todos os Posts (Otimizado)'
    }
    return render(request, 'blog/post_list.html', context)


def post_detail(request, slug):
    """View de detalhes do post - versão SEM otimização"""
    post = get_object_or_404(Post, slug=slug, published=True)
    
    # Incrementa views de forma ineficiente
    post.increment_views()
    
    # Busca posts relacionados de forma ineficiente
    related_posts = Post.objects.filter(
        category=post.category, 
        published=True
    ).exclude(id=post.id)[:3]
    
    context = {
        'post': post,
        'related_posts': related_posts,
        'page_title': post.title
    }
    return render(request, 'blog/post_detail.html', context)


def post_detail_optimized(request, slug):
    """View de detalhes do post - versão OTIMIZADA"""
    post = get_object_or_404(
        Post.objects.select_related('author', 'category'), 
        slug=slug, 
        published=True
    )
    
    # Incrementa views de forma eficiente (usando F)
    Post.objects.filter(id=post.id).update(views_count=F('views_count') + 1)
    
    # Busca posts relacionados de forma eficiente
    related_posts = Post.objects.filter(
        category=post.category, 
        published=True
    ).exclude(id=post.id).select_related('author')[:3]
    
    context = {
        'post': post,
        'related_posts': related_posts,
        'page_title': post.title
    }
    return render(request, 'blog/post_detail.html', context)


@cache_page(60 * 5)  # Cache por 5 minutos
def category_posts(request, category_id):
    """View de posts por categoria"""
    category = get_object_or_404(Category, id=category_id)
    posts = Post.objects.filter(
        category=category, 
        published=True
    ).select_related('author').order_by('-created_at')
    
    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'category': category,
        'page_obj': page_obj,
        'page_title': f'Posts em {category.name}'
    }
    return render(request, 'blog/category_posts.html', context)


def api_posts(request):
    """API simples para retornar posts em JSON"""
    posts = Post.objects.filter(published=True)\
                       .select_related('author', 'category')\
                       .order_by('-created_at')[:20]
    
    data = []
    for post in posts:
        data.append({
            'id': post.id,
            'title': post.title,
            'slug': post.slug,
            'author': post.author.username,
            'category': post.category.name if post.category else None,
            'created_at': post.created_at.isoformat(),
            'views_count': post.views_count
        })
    
    return JsonResponse({'posts': data})


def slow_endpoint(request):
    """Endpoint intencionalmente lento para demonstrar problemas de performance"""
    # Simula processamento pesado
    time.sleep(random.uniform(1, 3))
    
    # Query ineficiente - busca todos os posts sem otimização
    posts_count = 0
    for post in Post.objects.all():
        if post.published:
            posts_count += 1
            # Acessa author sem select_related (N+1 problem)
            author_name = post.author.username
    
    return JsonResponse({
        'message': 'Processamento concluído',
        'posts_count': posts_count,
        'processing_time': 'Variável entre 1-3 segundos'
    })


@require_http_methods(["GET"])
def health_check(request):
    """Endpoint simples para health check"""
    return JsonResponse({'status': 'ok', 'message': 'Blog API is running'})
