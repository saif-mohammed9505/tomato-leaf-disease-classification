"""Streamlit entry point.  Run with:  streamlit run app.py"""
import streamlit as st
from PIL import UnidentifiedImageError

from src import config, preprocess, ui
from src.model import ModelService

st.set_page_config(page_title=config.APP_TITLE, page_icon="🍅", layout="wide")
ui.inject_css()


@st.cache_resource(show_spinner="Loading model…")
def get_model() -> ModelService:
    return ModelService(config.MODEL_PATH)


def load_model_or_stop() -> ModelService:
    try:
        return get_model()
    except FileNotFoundError:
        st.error(
            f"Model file not found. Put `tomato_leaf_disease.h5` in the `models/` folder "
            f"(expected at `{config.MODEL_PATH}`), then reload."
        )
    except ImportError:
        st.error("TensorFlow isn't installed. Run `pip install -r requirements.txt`, then restart.")
    except Exception as exc:  # noqa: BLE001 - show any load failure to the user
        st.error(f"The model couldn't be loaded: {exc}")
    st.stop()


def main() -> None:
    service = load_model_or_stop()
    height, width = service.image_size
    mode = "grayscale" if service.channels == 1 else "RGB"

    with st.sidebar:
        st.subheader("Settings")
        min_confidence = st.slider(
            "Minimum confidence",
            min_value=0.30,
            max_value=0.95,
            value=config.DEFAULT_MIN_CONFIDENCE,
            step=0.05,
            format="%.2f",
            help="Below this, the app says it isn't sure instead of naming a disease. "
            "Raise it to avoid wrong calls; lower it to always get a best guess.",
        )
        show_input = st.toggle(
            "Show what the model sees",
            value=False,
            help="Displays the resized image that is fed to the model. Useful for checking preprocessing.",
        )
        st.divider()
        st.caption(f"Model file: {service.path.name}")
        st.caption(f"Input size: {width} × {height} px, {mode}")
        st.caption(f"Classes: {service.output_units}")

    ui.render_header()
    left, right = st.columns([1.05, 1], gap="large")

    image = None
    with left:
        upload = st.file_uploader(
            "Leaf photo", type=config.ALLOWED_TYPES, label_visibility="collapsed"
        )
        if upload is None:
            st.caption("Best results: one leaf filling the frame, in daylight, on a plain background.")
        else:
            try:
                image = preprocess.load_image(upload)
            except (UnidentifiedImageError, OSError):
                st.error("That file can't be read as an image. Try a JPG or PNG photo of the leaf.")
        if image is not None:
            with st.container(key="leaf"):
                st.image(image, caption=f"{upload.name}, {image.width} × {image.height} px")

    with right:
        if image is None:
            ui.render_empty_state()
        else:
            with st.spinner("Running the model…"):
                prediction = service.predict(image)
            ui.render_result(prediction, min_confidence)
            with st.expander(f"See all {service.output_units} scores"):
                ui.render_all_scores(prediction)
            if show_input:
                st.image(prediction.model_input, caption=f"Model input, {width} × {height} px, {mode}")

    ui.render_fineprint()


main()
