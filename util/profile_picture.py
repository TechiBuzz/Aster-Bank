from PIL import Image
from customtkinter import CTkImage

import io


def image_to_bytes(image: Image) -> bytes:
    with io.BytesIO() as output:
        image.save(output, 'PNG')
        binary_data = output.getvalue()

        return binary_data


def bytes_to_ctk_image(img_bytes: bytes) -> CTkImage:
    img = Image.open(io.BytesIO(img_bytes))
    ctk_img = CTkImage(img, img)
    return ctk_img
