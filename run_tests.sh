#!/bin/bash

echo "🧪 Script Automatizado de Testes de Carga"
echo "=========================================="

# Verificar se o Django está rodando
if ! curl -s http://127.0.0.1:8000 > /dev/null; then
    echo "❌ Servidor Django não está rodando!"
    echo "   Execute: python manage.py runserver"
    exit 1
fi

echo "✅ Servidor Django detectado em http://127.0.0.1:8000"

# Função para executar teste
run_test() {
    local test_name="$1"
    local locustfile="$2"
    local users="$3"
    local spawn_rate="$4"
    local duration="$5"
    
    echo ""
    echo "🚀 Executando teste: $test_name"
    echo "   Arquivo: $locustfile"
    echo "   Usuários: $users"
    echo "   Spawn rate: $spawn_rate/s"
    echo "   Duração: $duration"
    echo ""
    
    locust -f "$locustfile" \
           --host=http://127.0.0.1:8000 \
           --users "$users" \
           --spawn-rate "$spawn_rate" \
           --run-time "$duration" \
           --headless \
           --csv="results/$(basename "$locustfile" .py)_$(date +%Y%m%d_%H%M%S)"
}

# Criar diretório para resultados
mkdir -p results

echo ""
echo "📊 Executando bateria de testes..."

# Teste 1: Básico - Low Load
run_test "Teste Básico (Carga Baixa)" "locustfile_basic.py" 20 5 "60s"

echo ""
echo "⏰ Pausa de 10 segundos entre testes..."
sleep 10

# Teste 2: Básico - Medium Load
run_test "Teste Básico (Carga Média)" "locustfile_basic.py" 50 10 "90s"

echo ""
echo "⏰ Pausa de 15 segundos entre testes..."
sleep 15

# Teste 3: Comparação de Performance
run_test "Teste de Comparação" "locustfile_comparison.py" 30 8 "120s"

echo ""
echo "⏰ Pausa de 10 segundos entre testes..."
sleep 10

# Teste 4: Stress Test
run_test "Teste de Stress" "locustfile_comparison.py" 100 20 "60s"

echo ""
echo "✅ Todos os testes concluídos!"
echo ""
echo "📊 Resultados salvos em: ./results/"
echo "📋 Para analisar os resultados:"
echo "   ls -la results/"
echo "   cat results/*_stats.csv"
echo ""
echo "🎯 Próximos passos:"
echo "1. Analise os arquivos CSV gerados"
echo "2. Compare métricas entre testes"
echo "3. Identifique gargalos de performance"
echo "4. Execute testes individuais para investigar mais:"
echo "   locust -f locustfile_basic.py --host=http://127.0.0.1:8000"
