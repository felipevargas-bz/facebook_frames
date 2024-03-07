from PIL import Image
from io import BytesIO


def apply_frame(photo, frame_name):
    frame_path = f"./frames/{frame_name}"

    photo_img = Image.open(photo)

    frame_img = Image.open(frame_path)

    depth_width, depth_height = photo_img.size

    frame_img = frame_img.resize((depth_width, depth_height))

    photo_img = photo_img.convert('RGBA')

    result_img = Image.alpha_composite(photo_img, frame_img)

    result_img = result_img.convert('RGB')

    result_bytesio = BytesIO()
    result_img.save(result_bytesio, format='JPEG')

    return result_bytesio.getvalue()

# @app.post("/elegir/marco", )
# async def overlay_photo(marco: Frames, tu_foto_del_perfil: UploadFile = File(...)):
#     print("Elegir marco")
#     frame_name = marco.value
#     photo_content = await tu_foto_del_perfil.read()
#
#     result = apply_frame(BytesIO(photo_content), marco)
#
#     return StreamingResponse(BytesIO(result), media_type="image/jpeg",
#                              headers={"Content-Disposition": f"attachment; filename={frame_name}_overlay.jpg"})