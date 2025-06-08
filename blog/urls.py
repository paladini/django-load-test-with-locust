from django.urls import path
from . import views

app_name = 'blog'

urlpatterns = [
    # Views principais
    path('', views.home, name='home'),
    path('posts/', views.post_list, name='post_list'),
    path('posts/optimized/', views.post_list_optimized, name='post_list_optimized'),
    path('post/<slug:slug>/', views.post_detail, name='post_detail'),
    path('post/<slug:slug>/optimized/', views.post_detail_optimized, name='post_detail_optimized'),
    path('category/<int:category_id>/', views.category_posts, name='category_posts'),
    
    # API endpoints
    path('api/posts/', views.api_posts, name='api_posts'),
    path('api/health/', views.health_check, name='health_check'),
    path('api/slow/', views.slow_endpoint, name='slow_endpoint'),
]
