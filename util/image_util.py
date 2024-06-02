import io

from PIL import Image, ImageOps, ImageDraw
from customtkinter import CTkImage


def open_image(img_path: str, size: tuple[int, int]) -> CTkImage:
    img = Image.open(img_path)
    return CTkImage(light_image=img, dark_image=img, size=size)


def circular_image(image: Image, size: tuple[int, int]) -> CTkImage | None:
    # Image operations
    ImageOps.exif_transpose(image)  # reset rotational data

    image.convert("RGBA")
    image.thumbnail(size)

    # Create a circular mask
    mask = Image.new('L', size, 0)
    draw = ImageDraw.Draw(mask)
    draw.ellipse((0, 0) + size, fill=255)

    # Apply the mask to the image
    output_image = ImageOps.fit(image, size, centering=(0.5, 0.5))
    output_image.putalpha(mask)

    return CTkImage(light_image=output_image, dark_image=output_image, size=size)


def image_to_bytes(image: Image) -> bytes:
    with io.BytesIO() as output:
        image.save(output, 'PNG')
        binary_data = output.getvalue()

        return binary_data


def bytes_to_ctk_image(img_bytes: bytes) -> CTkImage:
    img = Image.open(io.BytesIO(img_bytes))
    ctk_img = CTkImage(img, img)
    return ctk_img
