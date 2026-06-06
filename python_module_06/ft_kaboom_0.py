from alchemy.grimoire import light_spell_record


if __name__ == "__main__":
    try:
        print("=== Kaboom 0 ===")
        print("Using grimoire module directly")
        print(
            "Testing record light spell:",
            light_spell_record("Fantasy", "Earth, wind and fire")
        )
    except Exception as e:
        print(f"{e}")
