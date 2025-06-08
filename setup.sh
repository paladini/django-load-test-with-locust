#!/bin/bash

echo "🚀 Setup do Projeto Django + Locust para Testes de Carga"
echo "========================================================="

# Verificar se estamos em um ambiente virtual
if [[ "$VIRTUAL_ENV" != "" ]]; then
    echo "✅ Ambiente virtual detectado: $VIRTUAL_ENV"
else
    echo "⚠️  Recomenda-se usar um ambiente virtual!"
    echo "   Para criar: python -m venv venv && source venv/bin/activate"
    read -p "Continuar mesmo assim? (y/n): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
fi

# Instalar dependências
echo ""
echo "📦 Instalando dependências..."
pip install -r requirements.txt

# Fazer migrações
echo ""
echo "🗄️  Executando migrações do banco de dados..."
python manage.py makemigrations
python manage.py migrate

# Popular banco de dados
echo ""
echo "📊 Populando banco de dados com dados de exemplo..."
python manage.py shell < populate_db.py

# Coletar arquivos estáticos
echo ""
echo "📁 Coletando arquivos estáticos..."
python manage.py collectstatic --noinput

echo ""
echo "✅ Setup concluído com sucesso!"
echo ""
echo "🎯 Próximos passos:"
echo "1. Iniciar servidor Django: python manage.py runserver"
echo "2. Acessar: http://127.0.0.1:8000"
echo "3. Admin: http://127.0.0.1:8000/admin (admin/admin123)"
echo "4. Executar testes Locust: locust -f locustfile_basic.py --host=http://127.0.0.1:8000"
echo ""
echo "📚 Para mais detalhes, consulte o README.md"
