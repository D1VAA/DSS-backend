from fastapi import FastAPI, Query, Depends, Body
from fastapi.middleware.cors import CORSMiddleware
import aiohttp
from pydantic import BaseModel
import uuid

from src.modules.scrapper import simple_distance_scrapper
# Importa o modelo e a função de sessão
from src.database import get_db, Routes

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class QueryRoute(BaseModel):
    origin: str
    destination: str


class File(BaseModel):
    file: bytes


@app.get("/route")
async def get_route(
    origin=Query(...),
    destination=Query(...),
    db=Depends(get_db)
):

    # Validate types
    QueryRoute(origin=origin, destination=destination)

    route = db.query(Routes).filter_by(
        origin=origin, destination=destination).first()
    if route:
        return {"id": route.id}

    async with aiohttp.ClientSession() as session:
        distance: float = await simple_distance_scrapper(session,
                                                         origin,
                                                         destination)

        if not isinstance(distance, float):
            return {"error": "Failed to fetch distance"}

    try:
        new_route = Routes(
            id=str(uuid.uuid4()),
            origin=origin,
            destination=destination,
            distance=distance)
        db.add(new_route)
        db.commit()
    except Exception as e:
        db.rollback()
        return {"error": str(e)}

    return {"id": new_route.id, "distance": distance}


@app.get("/all-routes")
async def get_all_routes(db=Depends(get_db)):
    routes = db.query(Routes).all()
    return routes


@app.post("/upload")
async def send_file(file: bytes = Body(...)):
    File(file)
    print("Received: ", file, "\nFile Type: ", type(file))
    SheetHandler()
