from fastapi import FastAPI, HTTPException, Form, UploadFile, File
from fastapi.responses import JSONResponse
from function import apply_frame
from io import BytesIO
from fastapi.middleware.cors import CORSMiddleware
import os
from fastapi.responses import StreamingResponse
import uuid

app = FastAPI(description="Usa el marco tu team en Facebook", summary="Elige tu Team en Facebook")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/elegir/marco")
async def overlay_photo(
    marco: str = Form(...),
    tu_foto_del_perfil: UploadFile = File(...),
):
    frame_name = marco
    photo_content = tu_foto_del_perfil.file.read()

    # Resto de tu código para aplicar el marco y devolver la respuesta
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

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=int(os.environ.get("PORT", 8000)))
