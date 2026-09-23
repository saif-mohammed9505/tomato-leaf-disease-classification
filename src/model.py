"""Loads tomato_leaf_disease.h5 and turns an image into per-class probabilities."""
from dataclasses import dataclass
from pathlib import Path

import numpy as np
from PIL import Image

from . import config, knowledge, preprocess


@dataclass(frozen=True)
class Prediction:
    probabilities: tuple[tuple[str, float], ...]  # (class key, probability), model order
    model_input: Image.Image  # the image exactly as the model saw it

    @property
    def ranked(self) -> list[tuple[str, float]]:
        """All classes, most likely first."""
        return sorted(self.probabilities, key=lambda item: item[1], reverse=True)

    @property
    def top(self) -> tuple[str, float]:
        return self.ranked[0]


class ModelService:
    def __init__(self, path: Path):
        path = Path(path)
        if not path.exists():
            raise FileNotFoundError(path)

        import tensorflow as tf  # imported here so a missing install gives a clear error

        self.path = path
        self.model = tf.keras.models.load_model(path, compile=False)

        shape = self.model.input_shape
        if isinstance(shape, list):
            shape = shape[0]
        _, height, width, channels = shape
        self.image_size = (
            height or config.FALLBACK_IMAGE_SIZE[0],
            width or config.FALLBACK_IMAGE_SIZE[1],
        )
        self.channels = channels or 3

        self.output_units = self.model.output_shape[-1]
        if self.output_units != len(config.CLASS_KEYS):
            raise ValueError(
                f"The model has {self.output_units} outputs but CLASS_KEYS in src/config.py "
                f"lists {len(config.CLASS_KEYS)}. Make them match, in training order."
            )
        unknown = [key for key in config.CLASS_KEYS if key not in knowledge.INFO]
        if unknown:
            raise ValueError(f"CLASS_KEYS has entries missing from src/knowledge.py: {unknown}")

    def predict(self, img: Image.Image) -> Prediction:
        model_input = preprocess.resize_for_model(img, self.image_size, self.channels)
        batch = preprocess.to_batch(model_input)
        out = np.asarray(self.model.predict(batch, verbose=0))[0].astype("float64")

        if not np.isclose(out.sum(), 1.0, atol=1e-3):  # raw logits -> softmax
            e = np.exp(out - out.max())
            out = e / e.sum()

        return Prediction(
            probabilities=tuple(zip(config.CLASS_KEYS, (float(p) for p in out))),
            model_input=model_input,
        )
