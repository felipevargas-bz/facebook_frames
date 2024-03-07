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
