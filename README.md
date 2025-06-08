# Blog Django - Demonstração de Testes de Carga com Locust

Este projeto é um exemplo educacional que demonstra como implementar e executar testes de carga em aplicações Django usando a biblioteca Locust.

## 📋 Índice

- [Visão Geral](#visão-geral)
- [Instalação e Setup](#instalação-e-setup)
- [Estrutura do Projeto](#estrutura-do-projeto)
- [Como Executar](#como-executar)
- [Testes de Carga](#testes-de-carga)
- [Comparação de Performance](#comparação-de-performance)
- [Otimizações Implementadas](#otimizações-implementadas)
- [Interpretando Resultados](#interpretando-resultados)
- [Cenários de Teste](#cenários-de-teste)

## 🎯 Visão Geral

Este projeto demonstra:

- **Blog Django** simples com posts, categorias e usuários
- **Duas versões** de cada view: otimizada e não-otimizada
- **Scripts Locust** para diferentes cenários de teste
- **Métricas de performance** para comparação
- **Exemplos práticos** de otimização Django

### Funcionalidades do Blog

- ✅ Sistema de posts com categorias
- ✅ Múltiplos autores
- ✅ Paginação
- ✅ API REST simples
- ✅ Interface administrativa
- ✅ Views otimizadas vs não-otimizadas

## 🚀 Instalação e Setup

### Pré-requisitos

- Python 3.8+
- pip
- (Opcional) Ambiente virtual

### Setup Automático

```bash
# Clonar/baixar o projeto
cd django-load-test-with-locust

# Criar ambiente virtual (recomendado)
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate  # Windows

# Executar setup automático
./setup.sh
```

### Setup Manual

```bash
# Instalar dependências
pip install -r requirements.txt

# Migrações do banco
python manage.py makemigrations
python manage.py migrate

# Popular banco com dados de exemplo
python manage.py populatedb

# Coletar arquivos estáticos
python manage.py collectstatic --noinput
```

## 📁 Estrutura do Projeto

```
django-load-test-with-locust/
├── blog/                          # App principal do blog
│   ├── models.py                  # Models: Post, Category
│   ├── views.py                   # Views otimizadas e normais
│   ├── urls.py                    # URLs do blog
│   ├── admin.py                   # Interface administrativa
│   └── templates/blog/            # Templates HTML
├── blogproject/                   # Configurações Django
│   ├── settings.py                # Settings com otimizações
│   └── urls.py                    # URLs principais
├── locustfile_basic.py            # Testes básicos Locust
├── locustfile_comparison.py       # Testes de comparação
├── populate_db.py                 # Script para popular BD
├── setup.sh                      # Setup automático
├── requirements.txt               # Dependências Python
└── README.md                      # Esta documentação
```

## 🏃‍♂️ Como Executar

### 1. Iniciar o Servidor Django

```bash
python manage.py runserver
```

O blog estará disponível em: http://127.0.0.1:8000

### 2. Acessos Importantes

- **Homepage**: http://127.0.0.1:8000/
- **Posts**: http://127.0.0.1:8000/posts/
- **Admin**: http://127.0.0.1:8000/admin/
- **API**: http://127.0.0.1:8000/api/posts/

### 3. Credenciais

- **Admin**: `admin` / `admin123`
- **Usuários**: `joao`, `maria`, `carlos`, `ana`, `pedro` / `password123`

## 🧪 Testes de Carga

### Teste Básico

Execute testes básicos simulando usuários reais:

```bash
locust -f locustfile_basic.py --host=http://127.0.0.1:8000
```

Acesse a interface web do Locust: http://localhost:8089

**Configuração sugerida:**
- **Number of users**: 50-100
- **Spawn rate**: 10 users/second

### Teste de Comparação

Compare performance entre versões otimizadas e não-otimizadas:

```bash
locust -f locustfile_comparison.py --host=http://127.0.0.1:8000
```

### Teste Headless (Linha de Comando)

```bash
# Teste básico por 60 segundos
locust -f locustfile_basic.py --host=http://127.0.0.1:8000 \
       --users 50 --spawn-rate 10 --run-time 60s --headless

# Teste de comparação
locust -f locustfile_comparison.py --host=http://127.0.0.1:8000 \
       --users 100 --spawn-rate 20 --run-time 120s --headless
```

## ⚡ Comparação de Performance

### URLs para Comparação

| Tipo | URL Normal | URL Otimizada |
|------|------------|---------------|
| Lista de Posts | `/posts/` | `/posts/optimized/` |
| Detalhes do Post | `/post/{slug}/` | `/post/{slug}/optimized/` |

### Exemplo de Teste Manual

```bash
# Terminal 1: Iniciar Django
python manage.py runserver

# Terminal 2: Teste a versão normal
curl -w "@curl-format.txt" -s -o /dev/null http://127.0.0.1:8000/posts/

# Terminal 3: Teste a versão otimizada
curl -w "@curl-format.txt" -s -o /dev/null http://127.0.0.1:8000/posts/optimized/
```

Crie `curl-format.txt`:
```
     time_namelookup:  %{time_namelookup}\n
        time_connect:  %{time_connect}\n
     time_appconnect:  %{time_appconnect}\n
    time_pretransfer:  %{time_pretransfer}\n
       time_redirect:  %{time_redirect}\n
  time_starttransfer:  %{time_starttransfer}\n
                     ----------\n
          time_total:  %{time_total}\n
```

## 🔧 Otimizações Implementadas

### 1. Otimização de Queries

**❌ Versão Ineficiente:**
```python
def post_list(request):
    posts = Post.objects.filter(published=True)  # N+1 queries
    # Para cada post, busca author e category separadamente
```

**✅ Versão Otimizada:**
```python
def post_list_optimized(request):
    posts = Post.objects.filter(published=True)\
                       .select_related('author', 'category')  # 1 query apenas
```

### 2. Atualização Eficiente de Campos

**❌ Versão Ineficiente:**
```python
def increment_views(self):
    self.views_count += 1
    self.save()  # Atualiza todos os campos
```

**✅ Versão Otimizada:**
```python
Post.objects.filter(id=post.id).update(views_count=F('views_count') + 1)
# Atualiza apenas o campo necessário no banco
```

### 3. Cache de Views

```python
@cache_page(60 * 5)  # Cache por 5 minutos
def category_posts(request, category_id):
    # View cached automaticamente
```

### 4. Índices no Banco

```python
class Post(models.Model):
    class Meta:
        indexes = [
            models.Index(fields=['-created_at']),
            models.Index(fields=['published']),
            models.Index(fields=['slug']),
        ]
```

## 📊 Interpretando Resultados

### Métricas Importantes

1. **RPS (Requests Per Second)**
   - Quantas requisições por segundo o servidor consegue processar
   - Maior = melhor

2. **Response Time**
   - Tempo médio de resposta
   - Observe percentis 50%, 95%, 99%
   - Menor = melhor

3. **Failure Rate**
   - Porcentagem de requisições que falharam
   - Idealmente 0%

4. **Concurrent Users**
   - Quantos usuários simultâneos o sistema suporta
   - Maior = melhor

### Exemplo de Resultados Esperados

```
Versão NÃO Otimizada:
- RPS: ~50-100
- Response Time (avg): 200-500ms
- Response Time (95%): 800-1500ms

Versão OTIMIZADA:
- RPS: ~200-400
- Response Time (avg): 50-150ms
- Response Time (95%): 200-400ms
```

### O que Observar

1. **Diferença de Performance**: Compare RPS e tempo de resposta
2. **Ponto de Quebra**: Em quantos usuários o sistema começa a falhar?
3. **Escalabilidade**: Como a performance degrada com mais usuários?
4. **Estabilidade**: Sistema mantém performance consistente?

## 🎭 Cenários de Teste

### 1. Usuário Navegador Típico (locustfile_basic.py)

- Visita homepage
- Navega por posts
- Lê alguns posts
- Comportamento realístico

### 2. Comparação de Performance (locustfile_comparison.py)

- Testa versões otimizadas vs não-otimizadas
- Identifica gargalos
- Mede impacto das otimizações

### 3. Usuário API

- Foca em endpoints da API
- Testa performance de JSON
- Simula aplicações mobile/SPA

### 4. Stress Test

- Requisições muito rápidas
- Identifica limite máximo
- Testa recuperação após picos

## 🎯 Demonstração Passo a Passo

### Para Apresentação

1. **Mostrar o Blog Funcionando**
   ```bash
   python manage.py runserver
   # Demonstrar navegação manual
   ```

2. **Executar Teste Básico**
   ```bash
   locust -f locustfile_basic.py --host=http://127.0.0.1:8000
   # Mostrar interface web, iniciar com 10-20 usuários
   ```

3. **Comparar Performance**
   ```bash
   # Acessar ambas as URLs durante o teste:
   # /posts/ (normal)
   # /posts/optimized/ (otimizada)
   ```

4. **Mostrar Métricas**
   - Charts em tempo real
   - Diferença nos tempos de resposta
   - RPS comparison

5. **Explicar Otimizações**
   - Mostrar código das views
   - Debug toolbar com queries
   - Impacto no banco de dados

## 🔍 Debug e Monitoramento

### Django Debug Toolbar

Acesse qualquer página com `?debug` para ver:
- Queries executadas
- Tempo de cada query
- Templates renderizados
- Cache hits/misses

### Logs de Performance

```bash
tail -f django.log  # Ver queries do banco em tempo real
```

### Comandos Úteis

```bash
# Ver estrutura do banco
python manage.py dbshell
.schema blog_post

# Analisar queries
python manage.py shell
>>> from blog.models import Post
>>> Post.objects.filter(published=True).explain()
```

## 🚨 Problemas Comuns

### Django Overwhelmed

**Sintoma**: Muitos erros 500, timeouts
**Solução**: Reduzir número de usuários, verificar configurações

### Banco de Dados Lento

**Sintoma**: Queries muito lentas
**Solução**: Verificar índices, otimizar queries, usar select_related

### Memory Issues

**Sintoma**: Sistema lento, swap usage
**Solução**: Implementar paginação, reduzir objetos em memória

### Connection Errors

**Sintoma**: "Connection refused" errors
**Solução**: Verificar `ALLOWED_HOSTS`, firewall, server running

## 📚 Recursos Adicionais

- [Documentação Django Performance](https://docs.djangoproject.com/en/stable/topics/performance/)
- [Locust Documentation](https://docs.locust.io/)
- [Django Debug Toolbar](https://django-debug-toolbar.readthedocs.io/)
- [Database Optimization](https://docs.djangoproject.com/en/stable/topics/db/optimization/)

## 🤝 Contribuições

Este é um projeto educacional. Sugestões de melhorias:

1. Adicionar mais cenários de teste
2. Implementar métricas customizadas
3. Adicionar configurações de produção
4. Incluir testes com PostgreSQL/Redis
5. Dockerização do projeto

## 📄 Licença

Este projeto é apenas para fins educacionais e demonstrações.

---

**💡 Dica**: Execute primeiro os testes básicos para entender o comportamento, depois compare as versões otimizadas para ver o impacto real das melhorias!
