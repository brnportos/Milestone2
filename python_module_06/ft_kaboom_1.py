if __name__ == "__main__":
    try:
        print("=== Kaboom 1 ===")
        print("Access to alchemy/grimoire/dark_spellbook.py directly")
        print("Test import now - THIS WILL RAISE AN UNCAUGHT EXCEPTION")
    except Exception as e:
        print(f"{e}")
from alchemy.grimoire.dark_spellbook import dark_spell_record
__all__ = ["dark_spell_record"]
