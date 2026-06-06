from ..elements import create_air
from ..potions import strength_potion
import elements


def lead_to_gold() -> str:
    return (
        f"Recipe transmuting Lead to Gold: brew ’{create_air()}’"
        f"and ’{strength_potion()}’ mixed with ’{elements.create_fire()}’"
        )
