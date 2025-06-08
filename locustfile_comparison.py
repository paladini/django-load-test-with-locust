"""
Teste de Comparação de Performance - Versões Otimizadas vs Não Otimizadas
Compare diretamente o impacto das otimizações
"""

from locust import HttpUser, task, between
import random

class PerformanceComparisonUser(HttpUser):
    wait_time = between(1, 2)
    
    @task(3)
    def test_unoptimized_posts(self):
        """Testa a versão NÃO otimizada da lista de posts"""
        response = self.client.get("/posts/", name="posts_unoptimized")
        
        # Simula paginação
        if random.random() < 0.5:
            page = random.randint(2, 10)
            self.client.get(f"/posts/?page={page}", name="posts_unoptimized_paginated")
    
    @task(3)
    def test_optimized_posts(self):
        """Testa a versão OTIMIZADA da lista de posts"""
        response = self.client.get("/posts/optimized/", name="posts_optimized")
        
        # Simula paginação
        if random.random() < 0.5:
            page = random.randint(2, 10)
            self.client.get(f"/posts/optimized/?page={page}", name="posts_optimized_paginated")
    
    @task(2)
    def test_unoptimized_post_detail(self):
        """Testa detalhes de post NÃO otimizados"""
        post_slugs = [
            'post-exemplo-50', 'post-exemplo-49', 'post-exemplo-48',
            'post-exemplo-47', 'post-exemplo-46', 'post-exemplo-45'
        ]
        slug = random.choice(post_slugs)
        self.client.get(f"/post/{slug}/", name="post_detail_unoptimized")
    
    @task(2)
    def test_optimized_post_detail(self):
        """Testa detalhes de post OTIMIZADOS"""
        post_slugs = [
            'post-exemplo-50', 'post-exemplo-49', 'post-exemplo-48',
            'post-exemplo-47', 'post-exemplo-46', 'post-exemplo-45'
        ]
        slug = random.choice(post_slugs)
        self.client.get(f"/post/{slug}/optimized/", name="post_detail_optimized")
    
    @task(1)
    def test_slow_endpoint(self):
        """Testa endpoint intencionalmente lento"""
        with self.client.get("/api/slow/", catch_response=True, name="slow_endpoint") as response:
            if response.status_code == 200:
                response.success()
            elif response.status_code == 500:
                response.failure("Server Error")

class RealisticUser(HttpUser):
    """Usuário com comportamento mais realístico"""
    wait_time = between(3, 8)
    weight = 5  # Mais comum
    
    def on_start(self):
        """Simula chegada de novo usuário"""
        self.client.get("/", name="new_visitor_homepage")
    
    @task(4)
    def typical_browsing_session(self):
        """Sessão típica de navegação"""
        # 1. Visita homepage
        self.client.get("/", name="session_homepage")
        
        # 2. Navega pelos posts
        self.client.get("/posts/", name="session_posts")
        
        # 3. Lê um post específico (50% chance)
        if random.random() < 0.5:
            post_slugs = ['post-exemplo-50', 'post-exemplo-49', 'post-exemplo-48']
            slug = random.choice(post_slugs)
            self.client.get(f"/post/{slug}/", name="session_read_post")
            
            # 4. Pode ler mais um post relacionado (30% chance)
            if random.random() < 0.3:
                slug = random.choice(post_slugs)
                self.client.get(f"/post/{slug}/", name="session_related_post")
    
    @task(1)
    def api_exploration(self):
        """Usuário curioso testando APIs"""
        self.client.get("/api/posts/", name="curious_api_check")
