# workshop-backend

Minimal FastAPI + SQLModel + Postgres todo API.

## Run

```bash
docker compose up -d          # starts database on localhost:5432
pip install -r requirements.txt
uvicorn main:app --reload
```

API docs: http://localhost:8000/docs

## Connect to Postgres

```bash
docker compose exec db psql -U postgres -d todos
# or, using a local psql client:
psql -h localhost -p 5432 -U postgres -d todos
```

## Endpoints

- `GET /todos` — list todos
- `POST /todos` — create todo, body: `{"title": "..."}`
- `PATCH /todos/{id}` — toggle done
- `DELETE /todos/{id}` — delete todo
