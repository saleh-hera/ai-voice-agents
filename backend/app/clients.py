from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Client
from app.schemas import ClientCreate, ClientOut

router = APIRouter()


@router.post("/client", response_model=ClientOut)
def create_client(payload: ClientCreate, db: Session = Depends(get_db)):
    if db.get(Client, payload.id):
        raise HTTPException(status_code=409, detail=f"client '{payload.id}' already exists")

    client = Client(
        id=payload.id,
        name=payload.name,
        industry=payload.industry,
        phone=payload.phone,
        email=payload.email,
        timezone=payload.timezone,
        business_data=payload.business_data,
        modules={k: v.model_dump() for k, v in payload.modules.items()},
        integrations=payload.integrations,
        tier=payload.tier,
        monthly_price_usd=payload.monthly_price_usd,
        status="trial",
    )
    db.add(client)
    db.commit()
    db.refresh(client)
    return client


@router.get("/client/{client_id}", response_model=ClientOut)
def get_client(client_id: str, db: Session = Depends(get_db)):
    client = db.get(Client, client_id)
    if not client:
        raise HTTPException(status_code=404, detail="not found")
    return client


@router.get("/clients", response_model=list[ClientOut])
def list_clients(db: Session = Depends(get_db)):
    return db.query(Client).all()


@router.put("/client/{client_id}", response_model=ClientOut)
def update_client(client_id: str, payload: ClientCreate, db: Session = Depends(get_db)):
    client = db.get(Client, client_id)
    if not client:
        raise HTTPException(status_code=404, detail="not found")

    client.name = payload.name
    client.industry = payload.industry
    client.phone = payload.phone
    client.email = payload.email
    client.timezone = payload.timezone
    client.business_data = payload.business_data
    client.modules = {k: v.model_dump() for k, v in payload.modules.items()}
    client.integrations = payload.integrations
    client.tier = payload.tier
    client.monthly_price_usd = payload.monthly_price_usd

    db.commit()
    db.refresh(client)
    return client
