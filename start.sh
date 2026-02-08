#!/bin/bash

echo "🚴 Strava Fenix - Setup Helper"
echo "=============================="
echo ""

# Check if .env exists
if [ ! -f .env ]; then
    echo "⚠️  No se encontró el archivo .env"
    echo "📝 Creando .env desde .env.example..."
    cp .env.example .env
    echo "✅ Archivo .env creado"
    echo ""
    echo "🔧 IMPORTANTE: Edita el archivo .env con tus credenciales de Strava:"
    echo "   - STRAVA_CLIENT_ID"
    echo "   - STRAVA_CLIENT_SECRET"
    echo "   - STRAVA_ACCESS_TOKEN"
    echo "   - STRAVA_CLUB_ID"
    echo ""
    echo "📖 Instrucciones en: https://www.strava.com/settings/api"
    echo ""
    read -p "Presiona Enter cuando hayas configurado el archivo .env..."
fi

echo "🔍 Verificando configuración..."
if grep -q "your_client_id_here" .env; then
    echo ""
    echo "❌ ERROR: Aún no has configurado tus credenciales de Strava en .env"
    echo "Por favor edita el archivo .env antes de continuar."
    exit 1
fi

echo "✅ Configuración lista"
echo ""
echo "🐳 Levantando servicios con Docker..."
docker-compose up --build
