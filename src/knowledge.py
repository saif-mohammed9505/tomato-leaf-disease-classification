"""Plain-language notes shown with each result.

Edit freely. General guidance only: local conditions, regulations and available
products differ, so an agricultural extension office should have the final word.
"""
from dataclasses import dataclass


@dataclass(frozen=True)
class DiseaseInfo:
    name: str
    kind: str  # shown as a small label: "Fungal disease", "Viral disease", ...
    look_for: str
    actions: tuple[str, ...]


INFO: dict[str, DiseaseInfo] = {
    "bacterial_spot": DiseaseInfo(
        name="Bacterial spot",
        kind="Bacterial disease",
        look_for=(
            "Small, dark, water-soaked spots on the leaves, often with a yellow halo. "
            "The spots can turn scabby, and the disease also reaches stems and fruit."
        ),
        actions=(
            "Remove badly affected leaves and bag them. Do not compost them.",
            "Water at the base and avoid working among wet plants.",
            "Use clean seed and transplants, and rotate away from tomato and pepper for a couple of years.",
            "Copper sprays can slow the spread but rarely stop it once it has taken hold.",
        ),
    ),
    "early_blight": DiseaseInfo(
        name="Early blight",
        kind="Fungal disease",
        look_for=(
            "Brown spots with concentric rings, like a target, usually on the older, lower "
            "leaves first. The leaf tissue around each spot often turns yellow."
        ),
        actions=(
            "Pick off and bag the infected lower leaves.",
            "Mulch the soil, and stake or prune the plants so air can move through them.",
            "Water at the base, in the morning.",
            "Rotate crops. If it keeps spreading, use a fungicide labelled for tomatoes.",
        ),
    ),
    "late_blight": DiseaseInfo(
        name="Late blight",
        kind="Fungal-like disease",
        look_for=(
            "Large, greasy-looking grey-green to brown blotches that spread fast in cool, wet "
            "weather. White fuzzy growth may show on the underside of the leaf."
        ),
        actions=(
            "Act quickly. Remove and bag infected plants, because it can reach nearby tomatoes "
            "and potatoes within days.",
            "Do not compost infected material.",
            "Avoid overhead watering and keep the foliage dry.",
            "Protective sprays only work before or very early in an outbreak. Ask your local "
            "agriculture office what is advised in your area.",
        ),
    ),
    "leaf_mold": DiseaseInfo(
        name="Leaf mold",
        kind="Fungal disease",
        look_for=(
            "Pale green or yellow patches on the upper side of the leaf, with a velvety "
            "olive-green to brown mold underneath. Common where it is humid and airflow is poor, "
            "such as in greenhouses."
        ),
        actions=(
            "Lower the humidity: ventilate and space the plants further apart.",
            "Keep the leaves dry and remove the affected ones.",
            "Choose resistant varieties next season.",
        ),
    ),
    "septoria_leaf_spot": DiseaseInfo(
        name="Septoria leaf spot",
        kind="Fungal disease",
        look_for=(
            "Many small round spots with dark edges and grey or tan centres, sometimes with "
            "tiny black dots in the middle. It starts on the lower leaves."
        ),
        actions=(
            "Remove affected lower leaves and bag them.",
            "Mulch so soil does not splash onto the leaves, and water at the base.",
            "Clear plant debris at the end of the season and rotate crops.",
        ),
    ),
    "spider_mites": DiseaseInfo(
        name="Spider mites",
        kind="Pest damage",
        look_for=(
            "Fine yellow speckling that can turn bronze, often with thin webbing on the "
            "underside of the leaf. Worst in hot, dry weather."
        ),
        actions=(
            "Look at the underside of the leaves for tiny moving dots before you treat anything.",
            "Spray the undersides with a strong jet of water, or use insecticidal soap or horticultural oil.",
            "Keep the plants well watered, since drought-stressed plants are hit hardest.",
        ),
    ),
    "target_spot": DiseaseInfo(
        name="Target spot",
        kind="Fungal disease",
        look_for=(
            "Brown spots with rings and a yellow halo, which can look a lot like early blight. "
            "It can affect leaves, stems and fruit."
        ),
        actions=(
            "Remove affected leaves and clear away fallen debris.",
            "Stake and prune for airflow, and avoid wetting the leaves.",
            "Rotate crops. A fungicide labelled for tomatoes can help if it keeps spreading.",
        ),
    ),
    "yellow_leaf_curl_virus": DiseaseInfo(
        name="Yellow leaf curl virus",
        kind="Viral disease",
        look_for=(
            "Leaves curl upward and turn yellow at the edges. Plants are stunted and set few "
            "fruit. Whiteflies spread it."
        ),
        actions=(
            "There is no cure. Remove and destroy infected plants.",
            "Control whiteflies with yellow sticky traps, reflective mulch or fine insect netting.",
            "Plant resistant or tolerant varieties next time.",
        ),
    ),
    "mosaic_virus": DiseaseInfo(
        name="Mosaic virus",
        kind="Viral disease",
        look_for=(
            "Mottled light and dark green patches. Leaves may be crinkled, narrow or fern-like, "
            "and the plant can be stunted."
        ),
        actions=(
            "There is no cure. Remove and destroy infected plants.",
            "Wash your hands and disinfect tools, since the virus spreads by touch and on tools.",
            "Use certified clean seed and resistant varieties.",
        ),
    ),
    "healthy": DiseaseInfo(
        name="Healthy leaf",
        kind="Healthy",
        look_for="No spots, curling, mottling or mold that this model knows how to recognise.",
        actions=(
            "Keep checking the undersides of the leaves every few days.",
            "Water at the base and keep air moving around the plants.",
        ),
    ),
}
