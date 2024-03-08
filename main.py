from fastapi import FastAPI, HTTPException, Form, UploadFile, File
from fastapi.responses import JSONResponse
from function import apply_frame
from io import BytesIO
from fastapi.middleware.cors import CORSMiddleware
import os
from fastapi.responses import StreamingResponse
import uuid
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, Integer, String, MetaData, Table
from databases import Database


# Configuración de la base de datos SQLite
DATABASE_URL = "sqlite:///./test.db"
database = Database(DATABASE_URL)
metadata = MetaData()

# Definir el modelo Team usando SQLAlchemy y Pydantic
teams = Table(
    "teams",
    metadata,
    Column("id", Integer, primary_key=True, index=True),
    Column("name", String, unique=True, index=True),
    Column("votes", Integer),
    Column("candidate", String),
    Column("photo", String),
)

engine = create_engine(DATABASE_URL)
metadata.create_all(engine)


app = FastAPI(description="Usa el marco tu team en Facebook", summary="Elige tu Team en Facebook")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class Team(BaseModel):
    name: str
    votes: int
    candidate: str
    photo: str


async def connect_db():
    await database.connect()

async def disconnect_db():
    await database.disconnect()


@app.post("/teams/")
async def create_team(team: Team):
    query = teams.insert().values(team.dict())
    team_id = await database.execute(query)
    return {"id": team_id, **team.dict()}


@app.get("/teams/")
async def get_teams():
    query = teams.select()
    return await database.fetch_all(query)


@app.put("/teams/vote/{team_name}")
async def vote_for_team(team_name: str):
    query = teams.update().where(teams.c.name == team_name).values({"votes": teams.c.votes + 1})
    updated_rows = await database.execute(query)

    if updated_rows == 0:
        raise HTTPException(status_code=404, detail="Equipo no encontrado")

    return {"message": f"Voto exitoso para el equipo {team_name}"}


@app.post("/elegir/marco")
async def overlay_photo(
    marco: str = Form(...),
    tu_foto_del_perfil: UploadFile = File(...),
):
    frame_name = marco
    photo_content = tu_foto_del_perfil.file.read()

    result = apply_frame(BytesIO(photo_content), frame_name)
    file_name = f"{uuid.uuid4().hex}.jpg"

    return StreamingResponse(BytesIO(result), media_type="image/jpeg",
                             headers={"Content-Disposition": f"attachment; filename={file_name}"})


@app.options("/elegir/marco")
async def preflight_marco():
    headers = {
        "Access-Control-Allow-Origin": "*",
        "Access-Control-Allow-Methods": "POST, OPTIONS",
    }
    return JSONResponse(content="ok", headers=headers)


@app.post("/subir_marco")
async def subir_frame(password: str, frame_name: str, marco: UploadFile = File(...)):
    if password != "987654321*":
        return {"error": "Incorrect password"}
    ruta_marco = os.path.join("./frames", f"{frame_name}.png")

    try:
        with open(ruta_marco, "wb") as buffer:
            buffer.write(marco.file.read())
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al subir el marco: {str(e)}")

    return JSONResponse(content={"mensaje": f"Marco {frame_name} subido exitosamente"})


# on_event is deprecated, use lifespan event handlers instead.

app.add_event_handler("startup", connect_db)
app.add_event_handler("shutdown", disconnect_db)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=int(os.environ.get("PORT", 8000)))
