from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse
from fastapi.responses import StreamingResponse
from function import apply_frame
from io import BytesIO
from enum import Enum
import os

app = FastAPI(description="Usa el marco tu team en Facebook", summary="Elige tu Team en Facebook")


class Frames(str, Enum):
    natty = "natty.png"
    caro = "caro.png"


@app.post("/elegir/marco", )
async def overlay_photo(marco: Frames, tu_foto_del_perfil: UploadFile = File(...)):
    frame_name = marco.value
    photo_content = await tu_foto_del_perfil.read()

    result = apply_frame(BytesIO(photo_content), marco)

    return StreamingResponse(BytesIO(result), media_type="image/jpeg", headers={"Content-Disposition": f"attachment; filename={frame_name}_overlay.jpg"})


@app.post("/subir_marco")
async def subir_frame(password: str, frame_name: str, marco: UploadFile = File(...)):
    if password != "<PASSWORD>":
        return JSONResponse
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
