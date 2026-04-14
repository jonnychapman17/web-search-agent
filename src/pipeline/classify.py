from __future__ import annotations


def classify_jurisdiction(text: str) -> str:
    lowered = text.lower()
    has_england = "england" in lowered
    has_wales = "wales" in lowered
    if has_england and has_wales:
        return "England and Wales"
    if has_wales:
        return "Wales"
    if has_england:
        return "England"
    return "Unknown"


def infer_audience(source_audience: str) -> str:
    if source_audience in {"official", "landlord", "tenant"}:
        return source_audience
    return "official"


def infer_category(audience: str) -> str:
    if audience == "landlord":
        return "landlord_concern"
    if audience == "tenant":
        return "tenant_concern"
    return "official_update"


def infer_theme(text: str) -> str:
    lowered = text.lower()
    theme_keywords = {
        "epc": ["epc", "energy performance", "mees"],
        "repairs_and_disrepair": ["repair", "repairs", "disrepair", "damp", "mould", "mold"],
        "licensing": ["licence", "license", "licensing", "hmo"],
        "rent_increase": ["rent increase", "increase rent", "rent rise", "section 13"],
        "arrears": ["arrears", "rent owed", "rent debt"],
        "possession_and_eviction": ["eviction", "possession", "section 8", "section 21", "notice seeking possession"],
        "deposits": ["deposit", "tenancy deposit", "deposit scheme"],
        "pets": ["pet", "pets"],
        "compliance": ["compliance", "gas safety", "eicr", "right to rent"],
        "tax_and_finance": ["tax", "mortgage", "finance", "stamp duty"],
        "anti_social_behaviour": ["anti-social", "antisocial", "nuisance"],
        "tenancy_setup": ["tenancy", "contract-holder", "contract holder", "agreement"],
        "tribunal_and_enforcement": ["tribunal", "court", "enforcement", "ombudsman"],
        "benefits_and_affordability": ["universal credit", "housing benefit", "affordability", "benefits"],
    }
    for theme, keywords in theme_keywords.items():
        if any(keyword in lowered for keyword in keywords):
            return theme
    return "other"
