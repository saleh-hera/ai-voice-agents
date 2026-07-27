from fastapi import FastAPI

from app.clients import router as clients_router
from app.database import Base, engine
from app.stripe_webhooks import router as stripe_webhooks_router
from app.webhooks import router as webhooks_router

# Creates tables on first run if they don't exist yet — fine for SQLite;
# switch to a real migration tool (Alembic) once this moves to Postgres.
Base.metadata.create_all(bind=engine)

app = FastAPI(title="AI Digital Dealer — Engine")

app.include_router(clients_router)
app.include_router(webhooks_router)
app.include_router(stripe_webhooks_router)


@app.get("/health")
def health():
    return {"status": "ok"}
