from fastapi import FastAPI, Query, Depends
from typing import Optional, Dict
import asyncio
import aiohttp
from pydantic import BaseModel
import uuid

from src.modules.scrapper import simple_distance_scrapper
from ..database import get_db, Routes  # Importa o modelo e a função de sessão

app = FastAPI()

class Query(BaseModel):
    origin: str
    destination: str

    def get_id(self) -> str:
        return str(uuid.uuid4())

@app.get("/route")
async def get_route(
    origin = Query (..., description="Origin address"),
    destination = Query (..., description="Destination address"),
    db = Depends(get_db)
    ):

    query = Query(origin=origin, destination=destination)
    q_id = query.get_id()

    route = db.query(Routes).filter_by(origin=origin, destination=destination).first()
    if route:
        return {"id": route.id}

@app.get("/all-routes")
async def get_all_routes(db = Depends(get_db)):
    routes = db.query(Routes).all()
    return routes
