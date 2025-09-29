# Jarvis 
## FastAPI + MongoDB CRUD

A production-ready, minimal FastAPI application that exposes CRUD endpoints backed by MongoDB (via Motor). Made for EKS Deployment practice

## Quickstart

### 1) Clone and set up

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
```

Edit `.env` as needed.

### 2) Run the API

```bash
uvicorn app.main:app --reload
```

Visit: http://127.0.0.1:8000/docs

### 3) Docker (optional)

```bash
docker compose up --build
```

This starts MongoDB and the app (ports 8000 for API).

---

## API Overview

`Item` model:

```json
{
  "id": "60ddc2c2c2c2c2c2c2c2c2c2",
  "name": "Sample",
  "description": "Optional text",
  "price": 9.99,
  "tags": ["a", "b"],
  "created_at": "2025-01-01T12:00:00Z",
  "updated_at": "2025-01-01T12:00:00Z"
}
```

Endpoints:

- `POST /items` – create
- `GET /items` – list (with `limit`, `skip`, and `q` filter)
- `GET /items/{id}` – get one
- `PUT /items/{id}` – replace (upsert=false)
- `PATCH /items/{id}` – partial update
- `DELETE /items/{id}` – delete

See `/docs` for full OpenAPI.

## Configuration

Environment variables (see `.env.example`):

- `MONGO_URI` – connection string (default: `mongodb://mongo:27017`)
- `DB_NAME` – database name (default: `appdb`)
- `COLLECTION_NAME` – collection name (default: `items`)