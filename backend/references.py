"""
Authoritative Reference Map
Maps each knowledge-base category to a trusted, authoritative medical
organisation where users can verify and read more. These are shown to the
user as "Learn more / verify" links alongside every answer, which is what
makes the assistant traceable and credible rather than a black box.

Note: these are pointers for verification and further reading by topic area;
they are not claims that the knowledge-base text was copied verbatim from
that page.
"""

# category -> {name, url}
CATEGORY_REFERENCES = {
    "cardiovascular": {
        "name": "American Heart Association",
        "url": "https://www.heart.org/en/health-topics",
    },
    "endocrine": {
        "name": "MedlinePlus — Diabetes & Hormones",
        "url": "https://medlineplus.gov/diabetes.html",
    },
    "respiratory": {
        "name": "American Lung Association",
        "url": "https://www.lung.org/lung-health-diseases",
    },
    "infectious": {
        "name": "CDC — Diseases & Conditions",
        "url": "https://www.cdc.gov/health-topics.html",
    },
    "neurological": {
        "name": "NIH — National Institute of Neurological Disorders",
        "url": "https://www.ninds.nih.gov/health-information/disorders",
    },
    "gastrointestinal": {
        "name": "NIH — Digestive Diseases (NIDDK)",
        "url": "https://www.niddk.nih.gov/health-information/digestive-diseases",
    },
    "oncology": {
        "name": "National Cancer Institute",
        "url": "https://www.cancer.gov/types",
    },
    "mental_health": {
        "name": "NIH — National Institute of Mental Health",
        "url": "https://www.nimh.nih.gov/health/topics",
    },
    "autoimmune": {
        "name": "MedlinePlus — Autoimmune Diseases",
        "url": "https://medlineplus.gov/autoimmunediseases.html",
    },
    "renal": {
        "name": "NIH — Kidney Disease (NIDDK)",
        "url": "https://www.niddk.nih.gov/health-information/kidney-disease",
    },
    "dermatology": {
        "name": "American Academy of Dermatology",
        "url": "https://www.aad.org/public/diseases",
    },
    "hematology": {
        "name": "American Society of Hematology",
        "url": "https://www.hematology.org/education/patients",
    },
    "immunology": {
        "name": "MedlinePlus — Immune System",
        "url": "https://medlineplus.gov/immunesystemanddisorders.html",
    },
    "ophthalmology": {
        "name": "American Academy of Ophthalmology",
        "url": "https://www.aao.org/eye-health",
    },
    "nutrition": {
        "name": "MedlinePlus — Nutrition",
        "url": "https://medlineplus.gov/nutrition.html",
    },
    "pharmacology": {
        "name": "MedlinePlus — Drugs & Supplements",
        "url": "https://medlineplus.gov/druginformation.html",
    },
    "women_health": {
        "name": "MedlinePlus — Women's Health",
        "url": "https://medlineplus.gov/womenshealth.html",
    },
    "pediatrics": {
        "name": "MedlinePlus — Children's Health",
        "url": "https://medlineplus.gov/childrenshealth.html",
    },
    "musculoskeletal": {
        "name": "NIH — Arthritis & Musculoskeletal (NIAMS)",
        "url": "https://www.niams.nih.gov/health-topics",
    },
    "first_aid": {
        "name": "MedlinePlus — First Aid",
        "url": "https://medlineplus.gov/firstaid.html",
    },
}

# Fallback for any category without a specific mapping.
DEFAULT_REFERENCE = {
    "name": "MedlinePlus (U.S. National Library of Medicine)",
    "url": "https://medlineplus.gov/",
}


def reference_for(category: str) -> dict:
    """Return the authoritative reference for a category, or a sensible default."""
    return CATEGORY_REFERENCES.get((category or "").lower(), DEFAULT_REFERENCE)
