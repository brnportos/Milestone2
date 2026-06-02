def validate_ingredients(ingredients: str, allowed: list[str]) -> str:
    lower_ingredients = ingredients.lower()
    valid = any(ingredient.lower() in lower_ingredients for ingredient in allowed)
    status = "VALID" if valid else "INVALID"
    return f"{ingredients} - {status}"
