"""Presentation helpers: styling, the result tag and the score list. No model logic here."""
from html import escape

import streamlit as st

from . import config, knowledge
from .model import Prediction


def _html(markup: str) -> str:
    # Collapse whitespace so Markdown never mistakes indented HTML for a code block.
    return " ".join(line.strip() for line in markup.splitlines())


def inject_css() -> None:
    css = config.STYLE_PATH.read_text(encoding="utf-8")
    st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)


def render_header() -> None:
    st.markdown(
        _html(
            f"""
            <header class="masthead">
              <div class="masthead__text">
                <h1>{config.APP_TITLE}</h1>
                <p>Upload a photo of one tomato leaf. The model names the most likely
                disease and what to do about it.</p>
              </div>
              <img class="masthead__image" alt="Home-grown tomatoes"
                   src="https://commons.wikimedia.org/wiki/Special:FilePath/Organic_home-grown_tomatoes_-_unripe_to_ripe.jpg" />
            </header>
            """
        ),
        unsafe_allow_html=True,
    )


def render_empty_state() -> None:
    st.markdown(
        _html(
            """
            <div class="empty">
              <img class="empty__image" alt="Tomato leaf damage in the field"
                   src="https://commons.wikimedia.org/wiki/Special:FilePath/Fig6-Enormous-tomato-losses-caused-by-Tuta-absoluta-in-Ngabobo-village.jpg" />
              <div>
                <strong>No leaf yet</strong>
                Upload a tomato leaf photo to see the diagnosis here.
              </div>
            </div>
            """
        ),
        unsafe_allow_html=True,
    )


def _score_rows(prediction: Prediction, limit: int | None) -> str:
    rows = []
    for i, (key, prob) in enumerate(prediction.ranked[:limit]):
        kind = "healthy" if key == config.HEALTHY_KEY else "disease"
        strong = " scores__row--top" if i == 0 else ""
        rows.append(
            f'<li class="scores__row{strong}">'
            f'<span class="scores__name">{escape(knowledge.INFO[key].name)}</span>'
            f'<span class="scores__bar"><span class="scores__fill scores__fill--{kind}" '
            f'style="width:{prob * 100:.1f}%"></span></span>'
            f'<span class="scores__pct">{prob * 100:.1f}%</span>'
            f"</li>"
        )
    return "".join(rows)


def render_result(prediction: Prediction, min_confidence: float) -> None:
    key, prob = prediction.top
    info = knowledge.INFO[key]
    pct = prob * 100

    if prob < min_confidence:
        state, title, chip = "unsure", "Not sure", "Low confidence"
        lead = (
            f"Best guess: {info.name} at {pct:.1f}%. That is under your "
            f"{min_confidence * 100:.0f}% minimum, so the model isn't calling it."
        )
        body = (
            '<p class="tag__tip">Try another photo: one leaf filling the frame, in daylight, '
            "on a plain background.</p>"
        )
    else:
        healthy = key == config.HEALTHY_KEY
        state = "healthy" if healthy else "disease"
        title, chip = info.name, info.kind
        lead = f"The model is {pct:.1f}% sure."
        look_heading, act_heading = (
            ("Result", "Keep it healthy") if healthy else ("What to look for", "What to do")
        )
        actions = "".join(f"<li>{escape(a)}</li>" for a in info.actions)
        body = (
            f'<h3 class="tag__heading">{look_heading}</h3>'
            f"<p>{escape(info.look_for)}</p>"
            f'<h3 class="tag__heading">{act_heading}</h3>'
            f'<ul class="tag__actions">{actions}</ul>'
        )

    st.markdown(
        _html(
            f"""
            <section class="tag tag--{state}" aria-live="polite">
              <span class="tag__chip tag__chip--{state}">{escape(chip)}</span>
              <h2 class="tag__title">{escape(title)}</h2>
              <p class="tag__lead">{escape(lead)}</p>
              {body}
            </section>
            <p class="scores__title">Closest matches</p>
            <ul class="scores">{_score_rows(prediction, limit=4)}</ul>
            """
        ),
        unsafe_allow_html=True,
    )


def render_all_scores(prediction: Prediction) -> None:
    st.markdown(
        _html(f'<ul class="scores">{_score_rows(prediction, limit=None)}</ul>'),
        unsafe_allow_html=True,
    )


def render_fineprint() -> None:
    st.markdown(
        _html(
            """
            <p class="fineprint">
              This is a quick aid, not an expert diagnosis. The model can't tell whether a photo
              really shows a tomato leaf, and models like this are usually trained on single
              leaves against plain backgrounds, so photos taken in the field can be less
              reliable. For a serious outbreak, contact your local agricultural extension service.
            </p>
            """
        ),
        unsafe_allow_html=True,
    )
