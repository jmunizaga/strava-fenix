# Strava Fenix - Rankings del Club

Aplicación web mobile-first para visualizar rankings semanales de tu club de Strava con clasificaciones por género y categorías UCI.

## 🚴 Características

- **Rankings Semanales**: Visualiza las métricas de la semana actual
- **Clasificación UCI**: Elite, Amateur, Master A/B/C/D
- **Filtros por Género**: Hombres, Mujeres, o todos
- **Métricas Principales**:
  - Distancia total recorrida
  - Altimetría acumulada
  - Recorrido más largo
- **Diseño Mobile-First**: Optimizado para visualización en teléfonos móviles
- **Interfaz Minimalista**: Inspirada en Strava con colores y tipografía premium

## 🛠️ Stack Tecnológico

- **Frontend**: Vue 3 + Vite + Tailwind CSS
- **Backend**: FastAPI (Python 3.11)
- **Containerización**: Docker + Docker Compose
- **API**: Strava API v3

## 📋 Prerequisitos

- Docker y Docker Compose instalados
- Cuenta de Strava con acceso a la API
- ID del club de Strava

## 🚀 Configuración Inicial

### 1. Obtener Credenciales de Strava

1. Ve a [Strava API Settings](https://www.strava.com/settings/api)
2. Crea una nueva aplicación si no tienes una
3. Anota tu **Client ID** y **Client Secret**
4. Para obtener el **Access Token**:
   - Puedes usar el token del navegador (temporal)
   - O implementar el flujo OAuth2 completo
5. Obtén el **Club ID** de la URL de tu club: `https://www.strava.com/clubs/{CLUB_ID}`

### 2. Configurar Variables de Entorno

```bash
cp .env.example .env
```

Edita `.env` con tus credenciales:

```env
STRAVA_CLIENT_ID=tu_client_id
STRAVA_CLIENT_SECRET=tu_client_secret
STRAVA_ACCESS_TOKEN=tu_access_token
STRAVA_CLUB_ID=tu_club_id
```

### 3. Levantar los Servicios

```bash
docker-compose up --build
```

La aplicación estará disponible en:
- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **Documentación API**: http://localhost:8000/docs

## 📱 Uso

1. Abre http://localhost:3000 en tu navegador (o en tu móvil si está en la misma red)
2. Selecciona los filtros:
   - **Género**: Todos, Hombres, o Mujeres
   - **Categoría**: General, Elite, Amateur, Master A/B/C/D
3. Visualiza el ranking actualizado de la semana

## 🏗️ Estructura del Proyecto

```
strava-fenix/
├── backend/                 # API FastAPI
│   ├── app/
│   │   ├── main.py         # Aplicación principal
│   │   ├── config.py       # Configuración
│   │   ├── models/         # Modelos Pydantic
│   │   ├── services/       # Lógica de negocio
│   │   └── routers/        # Endpoints API
│   └── Dockerfile
├── frontend/               # Aplicación Vue 3
│   ├── src/
│   │   ├── components/    # Componentes reutilizables
│   │   ├── views/         # Vistas principales
│   │   └── services/      # Cliente API
│   └── Dockerfile
└── docker-compose.yml     # Orquestación de servicios
```

## 🎨 Categorías UCI

- **Elite**: < 23 años
- **Amateur**: 23-29 años
- **Master A**: 30-39 años
- **Master B**: 40-49 años
- **Master C**: 50-59 años
- **Master D**: 60+ años

## 📊 API Endpoints

- `GET /api/rankings/weekly` - Obtener ranking semanal
  - Query params: `category`, `gender`, `week_offset`
- `GET /api/rankings/categories` - Listar categorías UCI disponibles
- `GET /health` - Health check

## 🔧 Desarrollo

### Backend
```bash
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload
```

### Frontend
```bash
cd frontend
npm install
npm run dev
```

## 📝 Notas

- El ranking se calcula desde el lunes de la semana actual
- Las actividades deben estar marcadas como públicas en Strava
- El access token de Strava puede expirar, necesitarás renovarlo periódicamente

## 🤝 Contribuciones

Este proyecto está diseñado específicamente para el club Fenix. Si deseas adaptarlo para tu club, simplemente configura tus propias credenciales de Strava.

## 📄 Licencia

MIT
