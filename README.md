# Weather Enrichment Service

---

**Table of Contents**
1. [Project Overview](#project-overview)
2. [Project Structure](#project-structure)
3. [Database Description](#database-description)
4. [Application Description](#application-description)
5. [How to Run the Project](#how-to-run-the-project)
   - [Prerequisites](#1-prerequisites)
   - [Running with Docker](#2-running-with-docker)
   - [Running Locally](#3-running-locally)
6. [Technologies](#technologies)

---

## Project Overview

Weather Enrichment Service is a full-stack application for managing cities and their real-time weather data. The backend exposes a REST API built with FastAPI that stores city records in PostgreSQL and fetches live weather information from the WeatherAPI via asynchronous Celery tasks backed by Redis.

The workflow includes:
1. Adding a city via the API or the Angular frontend
2. Automatically triggering an async Celery task to fetch weather data from WeatherAPI
3. Storing enriched weather data (temperature, humidity, wind, UV, etc.) in the database
4. Displaying and filtering cities with live weather in the Angular UI
5. Manually refreshing weather for any city on demand

---

## Project Structure

```text
weather-enrichment-service/
|-- backend/                          # FastAPI backend
|   |-- alembic/                      # Database migrations
|   |   `-- versions/                 # Migration scripts
|   |-- db/                           # SQLAlchemy engine, models
|   |   |-- engine.py                 # DB connection and session
|   |   `-- models.py                 # City and WeatherData models
|   |-- services/
|   |   `-- weather_api.py            # WeatherAPI HTTP client
|   |-- worker/                       # Celery async workers
|   |   |-- celery_app.py             # Celery app configuration
|   |   `-- tasks/
|   |       `-- weather_tasks.py      # update_weather_for_city task
|   |-- crud.py                       # Database CRUD helpers
|   |-- main.py                       # FastAPI app and routes
|   |-- schemas.py                    # Pydantic request/response schemas
|   |-- entrypoint.sh                 # Runs migrations then starts uvicorn
|   |-- Dockerfile
|   |-- requirements.txt
|   `-- .env.example
|-- frontend/                         # Angular frontend
|   |-- src/
|   |   |-- app/
|   |   |   |-- components/
|   |   |   |   `-- city-list/        # Cities table with search and sort
|   |   |   |-- models/
|   |   |   |   `-- city.model.ts     # City and Weather TypeScript interfaces
|   |   |   |-- services/
|   |   |   |   `-- city.service.ts   # HTTP service for backend API
|   |   |   |-- app.ts                # Root component with add-city form
|   |   |   `-- app.config.ts         # PrimeNG + HttpClient providers
|   |   |-- environments/
|   |   |   `-- environment.ts        # API URL configuration
|   |   `-- styles.scss               # Global styles
|   |-- nginx.conf                    # Nginx config for serving SPA
|   |-- Dockerfile
|   `-- .env.example
|-- docker-compose.yml
`-- README.md
```

---

## Database Description

The project uses PostgreSQL and includes two models managed via Alembic migrations:

- **City**
  - Stores city records added by the user
  - Fields: `id`, `name` (unique), `created_at`
  - One-to-one relationship with WeatherData (cascade delete)

- **WeatherData**
  - Stores the latest weather snapshot for a city
  - Fields: `id`, `city_id` (FK), `temperature`, `feels_like`, `humidity`, `description`, `wind_kph`, `pressure_mb`, `cloud`, `uv`, `updated_at`

Relationships:
- One `City` → one `WeatherData`

---

## Application Description

### Backend (FastAPI)

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | Health check |
| GET | `/cities` | List all cities with weather data |
| POST | `/cities` | Add a city and trigger weather fetch |
| POST | `/cities/{id}/refresh` | Trigger weather refresh for a city |

### Frontend (Angular + PrimeNG)

- Add a city by name — weather is fetched automatically in the background
- Paginated table of cities with full weather details
- Global search filtering by city name and weather description
- Sortable columns (temperature, humidity, wind, UV, etc.)
- Per-row Refresh button to re-fetch weather on demand
- Blue Aura PrimeNG theme

---

## How to Run the Project

### 1. Prerequisites

- Docker & Docker Compose
- (For local dev) Python 3.11+, Node.js 20+, a running PostgreSQL and Redis instance

---

### 2. Running with Docker

2.1. Clone the repository:

```bash
git clone https://github.com/mishagitcode/weather-enrichment-service
cd weather-enrichment-service
```

2.2. Set your WeatherAPI key in `backend/.env`:

```env
WEATHER_API_KEY=your_weatherapi_key_here
```

2.3. Start all services:

```bash
docker compose up --build
```

| Service | URL |
|---------|-----|
| Frontend | http://localhost:4200 |
| Backend API | http://localhost:8000 |
| API Docs | http://localhost:8000/docs |

---

### 3. Running Locally

3.1. **Backend**

```bash
cd backend
python -m venv venv
venv\Scripts\activate        # Windows
source venv/bin/activate     # macOS/Linux
pip install -r requirements.txt
```

Start PostgreSQL and Redis (or use Docker):

```bash
docker run -d --name weather_db -e POSTGRES_USER=postgres -e POSTGRES_PASSWORD=postgres -e POSTGRES_DB=weather_db -p 5432:5432 postgres:16
docker run -d --name weather_redis -p 6379:6379 redis:7
```

Run migrations and start the server:

```bash
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/weather_db alembic upgrade head
uvicorn main:app --reload
```

3.2. **Celery worker**

```bash
celery -A worker.celery_app.celery_app worker --loglevel=info -Q weather
```

3.3. **Frontend**

```bash
cd frontend
npm install
ng serve
```

Open http://localhost:4200

---

## Technologies

- **Python 3.11** — backend language
- **FastAPI** — REST API framework
- **SQLAlchemy** — ORM
- **Alembic** — database migrations
- **PostgreSQL** — primary database
- **Celery** — async task queue
- **Redis** — message broker and result backend
- **WeatherAPI** — external weather data source
- **Angular 21** — frontend framework
- **PrimeNG 21** — UI component library
- **Nginx** — static file serving for the Angular SPA
- **Docker / Docker Compose** — containerization

---

Developed by [mishagitcode](https://github.com/mishagitcode)
