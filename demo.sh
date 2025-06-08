#!/bin/bash

echo "🎯 DEMONSTRAÇÃO RÁPIDA - Blog Django + Locust"
echo "============================================="

# Verificar se o Django está rodando
if ! curl -s http://127.0.0.1:8000/api/health/ > /dev/null; then
    echo "❌ Servidor Django não está rodando!"
    echo "   Execute em outro terminal: python manage.py runserver"
    exit 1
fi

echo "✅ Servidor Django detectado"
echo ""

# Teste 1: Comparar performance de endpoints
echo "📊 TESTE 1: Comparação de Performance"
echo "------------------------------------"
echo "Testando versão NÃO otimizada..."
curl -w "@curl-format.txt" -s -o /dev/null http://127.0.0.1:8000/posts/

echo ""
echo "Testando versão OTIMIZADA..."
curl -w "@curl-format.txt" -s -o /dev/null http://127.0.0.1:8000/posts/optimized/

echo ""
echo "📈 Observe a diferença no 'time_total'!"
echo ""

# Teste 2: Locust básico
echo "🧪 TESTE 2: Locust - Carga Leve"
echo "-------------------------------"
echo "Executando teste com 10 usuários por 30 segundos..."
echo ""

locust -f locustfile_basic.py \
       --host=http://127.0.0.1:8000 \
       --users 10 \
       --spawn-rate 2 \
       --run-time 30s \
       --headless

echo ""
echo "✅ Demonstração concluída!"
echo ""
echo "🎯 Para demonstração completa:"
echo "1. Abra Locust web UI: locust -f locustfile_basic.py --host=http://127.0.0.1:8000"
echo "2. Acesse: http://localhost:8089"
echo "3. Configure: 50 usuários, spawn rate 10"
echo "4. Compare /posts/ vs /posts/optimized/ durante o teste"
echo ""
echo "📚 Consulte README.md para guia completo"
