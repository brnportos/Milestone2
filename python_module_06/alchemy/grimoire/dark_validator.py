from .dark_spellbook import dark_spell_allowed_ingredients


def validate_ingredients(ingredients: str) -> str:
    allowed = dark_spell_allowed_ingredients()
    lower = ingredients.lower()
    valid = any(item.lower() in lower for item in allowed)
    status = "VALID" if valid else "INVALID"
    return f"{ingredients} - {status}"
