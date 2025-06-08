"""
Django management command para popular o banco de dados com dados de exemplo
Execute: python manage.py populate_db
"""

from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.utils.text import slugify
from blog.models import Category, Post
import random


class Command(BaseCommand):
    help = 'Popula o banco de dados com dados de exemplo para testes'

    def handle(self, *args, **options):
        self.stdout.write("🚀 Iniciando população do banco de dados...")
        
        # Criar superusuário se não existir
        if not User.objects.filter(username='admin').exists():
            admin = User.objects.create_superuser(
                username='admin',
                email='admin@blog.com',
                password='admin123'
            )
            self.stdout.write(self.style.SUCCESS("✅ Superusuário 'admin' criado (senha: admin123)"))
        else:
            admin = User.objects.get(username='admin')
            self.stdout.write("✅ Superusuário 'admin' já existe")
        
        # Criar usuários adicionais
        authors = []
        author_names = ['joao', 'maria', 'carlos', 'ana', 'pedro']
        
        for name in author_names:
            if not User.objects.filter(username=name).exists():
                user = User.objects.create_user(
                    username=name,
                    email=f'{name}@blog.com',
                    password='password123',
                    first_name=name.title()
                )
                authors.append(user)
                self.stdout.write(self.style.SUCCESS(f"✅ Usuário '{name}' criado"))
            else:
                authors.append(User.objects.get(username=name))
        
        authors.append(admin)
        
        # Criar categorias
        categories_data = [
            {'name': 'Tecnologia', 'description': 'Posts sobre tecnologia e programação'},
            {'name': 'Django', 'description': 'Tutoriais e dicas sobre Django'},
            {'name': 'Performance', 'description': 'Otimização e performance de aplicações'},
            {'name': 'Testes', 'description': 'Testes de software e qualidade'},
            {'name': 'DevOps', 'description': 'Deploy, infraestrutura e operações'},
        ]
        
        categories = []
        for cat_data in categories_data:
            category, created = Category.objects.get_or_create(
                name=cat_data['name'],
                defaults={'description': cat_data['description']}
            )
            categories.append(category)
            if created:
                self.stdout.write(self.style.SUCCESS(f"✅ Categoria '{category.name}' criada"))
        
        # Criar posts de exemplo
        posts_data = [
            {
                'title': 'Primeiro Post do Blog',
                'content': '''Este é o primeiro post do nosso blog Django! 
                
Estamos criando este conteúdo para demonstrar como realizar testes de carga usando Locust. 

O Locust é uma ferramenta fantástica para simular usuários reais acessando sua aplicação web. 
Com ele, podemos identificar gargalos de performance antes que eles afetem usuários reais.

Neste post, vamos explorar:
- Como configurar testes básicos
- Métricas importantes para monitorar
- Interpretação dos resultados

Continue acompanhando nosso blog para mais conteúdos sobre performance e testes!'''
            },
            {
                'title': 'Introdução ao Django',
                'content': '''Django é um framework web de alto nível escrito em Python que encoraja o desenvolvimento rápido e limpo.

Principais características do Django:

1. **ORM Poderoso**: O Django inclui um Object-Relational Mapping que permite trabalhar com bancos de dados usando Python.

2. **Admin Interface**: Interface administrativa automática para gerenciar dados.

3. **Sistema de Templates**: Motor de templates flexível e poderoso.

4. **Sistema de URLs**: Roteamento de URLs limpo e elegante.

5. **Middleware**: Sistema de middleware para processamento de requests/responses.

Este blog foi construído com Django para demonstrar essas funcionalidades na prática!'''
            },
            {
                'title': 'Otimização de Queries Django',
                'content': '''Um dos pontos mais importantes para performance em Django é a otimização de queries do banco de dados.

**Problemas Comuns:**

- **N+1 Queries**: Quando você acessa relacionamentos sem usar select_related/prefetch_related
- **Queries Desnecessárias**: Buscar dados que não serão utilizados
- **Falta de Índices**: Queries lentas por falta de índices apropriados

**Soluções:**

1. **select_related()**: Para relacionamentos ForeignKey e OneToOne
2. **prefetch_related()**: Para relacionamentos ManyToMany e reverse ForeignKey
3. **only()** e **defer()**: Para controlar quais campos buscar
4. **Índices**: Adicionar índices apropriados nos modelos

Exemplo prático:
```python
# ❌ Ineficiente (N+1 queries)
posts = Post.objects.all()
for post in posts:
    print(post.author.username)  # Query para cada post

# ✅ Eficiente (2 queries apenas)
posts = Post.objects.select_related('author')
for post in posts:
    print(post.author.username)
```

No nosso blog, implementamos duas versões de cada view para demonstrar essa diferença!'''
            },
            {
                'title': 'Testes de Carga com Locust',
                'content': '''Locust é uma ferramenta de teste de carga fácil de usar e escalável.

**Por que usar Locust?**

- **Python**: Escreva testes em Python puro
- **Interface Web**: Monitore testes em tempo real
- **Distribuído**: Execute testes em múltiplas máquinas
- **Flexível**: Simule comportamentos complexos de usuários

**Conceitos Básicos:**

1. **HttpUser**: Classe base para simular usuários
2. **@task**: Decorador para definir ações dos usuários
3. **wait_time**: Tempo de espera entre ações
4. **weight**: Peso das tarefas (frequência)

**Exemplo Simples:**
```python
from locust import HttpUser, task, between

class WebsiteUser(HttpUser):
    wait_time = between(1, 3)
    
    @task
    def index_page(self):
        self.client.get("/")
        
    @task(3)  # 3x mais provável
    def view_posts(self):
        self.client.get("/posts/")
```

**Métricas Importantes:**
- **RPS**: Requests per Second
- **Response Time**: Tempo de resposta médio/percentis
- **Failure Rate**: Taxa de falhas
- **Concurrent Users**: Usuários simultâneos

Com Locust, você pode identificar o limite de sua aplicação antes que usuários reais sejam impactados!'''
            },
            {
                'title': 'Monitoramento de Performance Django',
                'content': '''Monitorar a performance de aplicações Django é essencial para manter uma boa experiência do usuário.

**Ferramentas de Monitoramento:**

1. **Django Debug Toolbar**: Para desenvolvimento
2. **Django Silk**: Profiling detalhado
3. **New Relic/Datadog**: Monitoramento em produção
4. **Sentry**: Tracking de erros

**Métricas Importantes:**

- **Response Time**: Tempo de resposta das views
- **Database Query Time**: Tempo gasto em queries
- **Memory Usage**: Uso de memória
- **Error Rate**: Taxa de erros

**Django Settings para Performance:**

```python
# Cache
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.redis.RedisCache',
        'LOCATION': 'redis://127.0.0.1:6379/1',
    }
}

# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'CONN_MAX_AGE': 600,  # Persistent connections
    }
}

# Compression
MIDDLEWARE = [
    'django.middleware.gzip.GZipMiddleware',
    # ... other middleware
]
```

**Dicas de Otimização:**

1. Use cache para dados que não mudam frequentemente
2. Otimize queries com select_related/prefetch_related
3. Implemente paginação adequada
4. Use CDN para assets estáticos
5. Configure compressão gzip

Lembre-se: "Premature optimization is the root of all evil" - otimize apenas onde há necessidade comprovada!'''
            }
        ]
        
        # Criar posts
        created_posts = []
        for i, post_data in enumerate(posts_data):
            author = random.choice(authors)
            category = random.choice(categories)
            
            slug = slugify(post_data['title'])
            
            post, created = Post.objects.get_or_create(
                slug=slug,
                defaults={
                    'title': post_data['title'],
                    'content': post_data['content'],
                    'author': author,
                    'category': category,
                    'published': True,
                    'views_count': random.randint(10, 1000)
                }
            )
            
            if created:
                created_posts.append(post)
                self.stdout.write(self.style.SUCCESS(f"✅ Post '{post.title}' criado"))
        
        # Criar posts adicionais para paginação
        lorem_content = """Lorem ipsum dolor sit amet, consectetur adipiscing elit. 
Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. 
Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. 

Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. 
Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.

Sed ut perspiciatis unde omnis iste natus error sit voluptatem accusantium doloremque laudantium, 
totam rem aperiam, eaque ipsa quae ab illo inventore veritatis et quasi architecto beatae vitae dicta sunt explicabo."""
        
        for i in range(6, 51):  # Criar posts 6-50
            title = f"Post de Exemplo #{i}"
            slug = f"post-exemplo-{i}"
            
            if not Post.objects.filter(slug=slug).exists():
                author = random.choice(authors)
                category = random.choice(categories)
                
                post = Post.objects.create(
                    title=title,
                    slug=slug,
                    content=f"{lorem_content}\n\nEste é o post número {i} criado para demonstração de paginação e testes de carga.",
                    author=author,
                    category=category,
                    published=True,
                    views_count=random.randint(1, 500)
                )
                created_posts.append(post)
        
        self.stdout.write(self.style.SUCCESS(f"✅ Total de {len(created_posts)} posts criados"))
        self.stdout.write(f"📊 Total de posts no banco: {Post.objects.count()}")
        self.stdout.write(f"📂 Total de categorias: {Category.objects.count()}")
        self.stdout.write(f"👥 Total de usuários: {User.objects.count()}")
        
        self.stdout.write(self.style.SUCCESS("\n🎉 Banco de dados populado com sucesso!"))
        self.stdout.write("\n📋 Credenciais de acesso:")
        self.stdout.write("   Admin: admin / admin123")
        self.stdout.write("   Usuários: joao, maria, carlos, ana, pedro / password123")
        
        self.stdout.write("\n🌐 URLs para testar:")
        self.stdout.write("   Homepage: /")
        self.stdout.write("   Posts: /posts/")
        self.stdout.write("   Posts Otimizados: /posts/optimized/")
        self.stdout.write("   API: /api/posts/")
        self.stdout.write("   Admin: /admin/")
