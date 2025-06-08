"""
Teste de Carga Básico - Blog Django
Simula usuários navegando pelo blog de forma realística
"""

from locust import HttpUser, task, between
import random


class BlogUser(HttpUser):
    wait_time = between(1, 3)  # Pausa entre 1-3 segundos entre requests
    
    def on_start(self):
        """Executado quando um usuário inicia a sessão"""
        # Simula visita inicial à homepage
        self.client.get("/", name="01_homepage")
    
    @task(5)  # Peso 5 - tarefa mais comum
    def browse_homepage(self):
        """Usuários visitam a homepage frequentemente"""
        self.client.get("/", name="01_homepage")
    
    @task(4)  # Peso 4
    def view_posts_list(self):
        """Usuários navegam pela lista de posts"""
        response = self.client.get("/posts/", name="02_posts_list")
        
        # Simula paginação ocasional
        if random.random() < 0.3:  # 30% chance
            page = random.randint(2, 5)
            self.client.get(f"/posts/?page={page}", name="02_posts_list_paginated")
    
    @task(3)  # Peso 3
    def view_post_detail(self):
        """Usuários leem posts específicos"""
        # Lista de slugs de exemplo (você pode adicionar mais)
        post_slugs = [
            'primeiro-post',
            'segundo-post', 
            'terceiro-post',
            'quarto-post',
            'quinto-post'
        ]
        
        slug = random.choice(post_slugs)
        self.client.get(f"/post/{slug}/", name="03_post_detail")
    
    @task(2)  # Peso 2
    def check_api_posts(self):
        """Alguns usuários acessam a API"""
        self.client.get("/api/posts/", name="04_api_posts")
    
    @task(1)  # Peso 1 - menos frequente
    def health_check(self):
        """Health check ocasional"""
        self.client.get("/api/health/", name="05_health_check")
    
    @task(1)  # Peso 1 - para demonstrar problemas
    def slow_endpoint(self):
        """Endpoint lento para demonstrar problemas de performance"""
        with self.client.get("/api/slow/", catch_response=True, name="06_slow_endpoint") as response:
            # Considera sucesso mesmo se demorar
            if response.status_code == 200:
                response.success()


class BrowsingUser(HttpUser):
    """Usuário que apenas navega sem usar APIs"""
    wait_time = between(2, 5)
    weight = 3  # 3x mais comum que outros tipos de usuário
    
    @task(10)
    def browse_only(self):
        """Navega apenas pelas páginas do blog"""
        pages = [
            "/",
            "/posts/",
            "/posts/?page=2"
        ]
        page = random.choice(pages)
        self.client.get(page, name="browser_navigation")


class APIUser(HttpUser):
    """Usuário que usa principalmente APIs"""
    wait_time = between(0.5, 2)
    weight = 1  # Menos comum
    
    @task(5)
    def api_calls(self):
        """Faz chamadas para API"""
        self.client.get("/api/posts/", name="api_usage")
        
    @task(1)
    def health_checks(self):
        """Health checks frequentes"""
        self.client.get("/api/health/", name="api_health")
