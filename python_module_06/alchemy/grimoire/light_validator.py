def validate_ingredients(ingredients: str) -> str:
    from .light_spellbook import light_spell_allowed_ingredients
    allowed = light_spell_allowed_ingredients()
    lower_ingredients: str = ingredients.lower()
    valid: bool = any(
        ingredient.lower() in lower_ingredients for ingredient in allowed
        )
    status: str = "VALID" if valid else "INVALID"
    return f"{ingredients} - {status}"
