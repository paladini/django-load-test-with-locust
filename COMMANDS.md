# Comandos Úteis - Blog Django + Locust

## Setup Inicial
```bash
# Criar ambiente virtual
python -m venv venv
source venv/bin/activate

# Instalar dependências
pip install -r requirements.txt

# Setup completo automático
./setup.sh
```

## Django
```bash
# Iniciar servidor de desenvolvimento
python manage.py runserver

# Fazer migrações
python manage.py makemigrations
python manage.py migrate

# Criar superusuário
python manage.py createsuperuser

# Popular banco de dados
python manage.py shell < populate_db.py

# Shell Django
python manage.py shell

# Resetar banco de dados
rm db.sqlite3
python manage.py migrate
python manage.py shell < populate_db.py
```

## Locust - Testes Básicos
```bash
# Interface web (recomendado para demonstrações)
locust -f locustfile_basic.py --host=http://127.0.0.1:8000

# Headless (linha de comando)
locust -f locustfile_basic.py --host=http://127.0.0.1:8000 \
       --users 50 --spawn-rate 10 --run-time 60s --headless

# Com resultados CSV
locust -f locustfile_basic.py --host=http://127.0.0.1:8000 \
       --users 30 --spawn-rate 5 --run-time 120s --headless \
       --csv=results/basic_test
```

## Locust - Testes de Comparação
```bash
# Interface web
locust -f locustfile_comparison.py --host=http://127.0.0.1:8000

# Teste de stress
locust -f locustfile_comparison.py --host=http://127.0.0.1:8000 \
       --users 100 --spawn-rate 20 --run-time 60s --headless
```

## Testes Automatizados
```bash
# Executar bateria completa de testes
./run_tests.sh

# Ver resultados
ls -la results/
cat results/*_stats.csv
```

## Análise de Performance
```bash
# Testar endpoints específicos
curl -w "@curl-format.txt" -s -o /dev/null http://127.0.0.1:8000/posts/
curl -w "@curl-format.txt" -s -o /dev/null http://127.0.0.1:8000/posts/optimized/

# Monitorar logs
tail -f django.log

# Ver queries do banco
python manage.py shell
>>> from django.db import connection
>>> from blog.models import Post
>>> len(connection.queries)
>>> Post.objects.filter(published=True)[:5]
>>> len(connection.queries)  # Ver quantas queries foram executadas
```

## URLs Importantes
```
Homepage:              http://127.0.0.1:8000/
Posts (normal):        http://127.0.0.1:8000/posts/
Posts (otimizado):     http://127.0.0.1:8000/posts/optimized/
Post detail:           http://127.0.0.1:8000/post/primeiro-post/
Post detail (otim):    http://127.0.0.1:8000/post/primeiro-post/optimized/
API Posts:             http://127.0.0.1:8000/api/posts/
API Health:            http://127.0.0.1:8000/api/health/
API Slow:              http://127.0.0.1:8000/api/slow/
Admin:                 http://127.0.0.1:8000/admin/
Locust UI:             http://127.0.0.1:8089/
```

## Credenciais
```
Admin:     admin / admin123
Usuários:  joao, maria, carlos, ana, pedro / password123
```

## Curl Format File (curl-format.txt)
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

## Troubleshooting
```bash
# Server não inicia
python manage.py check
python manage.py migrate

# Locust não conecta
# Verificar se Django está rodando:
curl http://127.0.0.1:8000

# Banco de dados corrompido
rm db.sqlite3
python manage.py migrate
python manage.py shell < populate_db.py

# Limpar cache
python manage.py shell
>>> from django.core.cache import cache
>>> cache.clear()

# Ver configuração atual
python manage.py diffsettings
```

## Demonstração para Apresentação
```bash
# Terminal 1: Django
python manage.py runserver

# Terminal 2: Locust
locust -f locustfile_basic.py --host=http://127.0.0.1:8000

# Terminal 3: Monitoramento
watch -n 1 "curl -s http://127.0.0.1:8000/api/health/ | jq"

# Browser 1: Blog
http://127.0.0.1:8000

# Browser 2: Locust UI
http://127.0.0.1:8089
```

## Cenários de Demonstração

### 1. Navegação Normal
- Mostrar blog funcionando
- Explicar funcionalidades

### 2. Teste Básico
- Locust com 10-20 usuários
- Mostrar métricas em tempo real

### 3. Comparação de Performance
- Testar /posts/ vs /posts/optimized/
- Mostrar diferença nos gráficos

### 4. Identificar Gargalos
- Testar /api/slow/
- Mostrar como falhas aparecem

### 5. Debug
- Django Debug Toolbar
- Mostrar queries executadas
