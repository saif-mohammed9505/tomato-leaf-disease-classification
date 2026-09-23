"""Turn an uploaded file into the array the model expects."""
import numpy as np
from PIL import Image, ImageOps

from . import config

_RESAMPLE = {
    "nearest": Image.Resampling.NEAREST,
    "bilinear": Image.Resampling.BILINEAR,
    "bicubic": Image.Resampling.BICUBIC,
    "lanczos": Image.Resampling.LANCZOS,
}


def load_image(file) -> Image.Image:
    """Open an uploaded file and fix its orientation. Raises if it isn't an image."""
    img = Image.open(file)
    img.load()  # force decoding now so bad files fail here, not later
    return ImageOps.exif_transpose(img)


def resize_for_model(img: Image.Image, size: tuple[int, int], channels: int) -> Image.Image:
    """Match the model's colour mode and (height, width)."""
    mode = "L" if channels == 1 else "RGB"
    height, width = size
    return img.convert(mode).resize((width, height), _RESAMPLE[config.RESIZE_METHOD])


def to_batch(img: Image.Image) -> np.ndarray:
    """PIL image -> float32 array shaped (1, height, width, channels)."""
    arr = np.asarray(img, dtype="float32")
    if arr.ndim == 2:
        arr = arr[..., np.newaxis]
    if config.RESCALE == "0-1":
        arr = arr / 255.0
    return arr[np.newaxis, ...]
