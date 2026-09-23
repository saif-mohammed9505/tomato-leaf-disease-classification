"""Every setting you might need to change lives here.

If the diagnoses look wrong, the cause is almost always a mismatch between
these settings and how the model was trained (see README, "Troubleshooting").
"""
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
MODEL_PATH = ROOT / "models" / "tomato_leaf_disease.h5"
STYLE_PATH = ROOT / "assets" / "style.css"

APP_TITLE = "Tomato leaf disease check"
ALLOWED_TYPES = ["png", "jpg", "jpeg", "bmp", "tif", "tiff", "webp"]

# ---- Preprocessing (must match what you did during training) ---------------

# Used only when the model does not report a fixed input size. (height, width)
FALLBACK_IMAGE_SIZE = (224, 224)

# "0-1"  : divide pixels by 255 (ImageDataGenerator(rescale=1/255), most tutorials)
# "none" : keep 0-255 (the model has its own Rescaling layer, or trained on raw pixels)
RESCALE = "0-1"

# "nearest", "bilinear", "bicubic" or "lanczos".
# Keras load_img / flow_from_directory default to nearest; cv2.resize defaults to bilinear.
RESIZE_METHOD = "bilinear"

# ---- What the model outputs mean -------------------------------------------

# One key per output unit, IN THE ORDER THE MODEL WAS TRAINED. Each key must exist
# in src/knowledge.py, which holds the display name and advice for it.
#
# Keras numbers class folders alphabetically. The list below is the order for the
# 10 standard tomato folders (Tomato___Bacterial_spot ... Tomato___healthy). To
# confirm, print `train_generator.class_indices` (or `class_names` from
# image_dataset_from_directory) in your training notebook.
CLASS_KEYS = [
    "bacterial_spot",
    "early_blight",
    "late_blight",
    "leaf_mold",
    "septoria_leaf_spot",
    "spider_mites",
    "target_spot",
    "yellow_leaf_curl_virus",
    "mosaic_virus",
    "healthy",
]

# Which key means "no disease".
HEALTHY_KEY = "healthy"

# Below this confidence the app says "Not sure" instead of naming a disease.
# Adjustable in the sidebar.
DEFAULT_MIN_CONFIDENCE = 0.60
