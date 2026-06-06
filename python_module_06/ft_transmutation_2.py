import alchemy.transmutation.recipes


if __name__ == "__main__":
    try:
        print("=== Transmutation 2 ===")
        print("Import alchemy module only")
        print(
            f"Testing lead to gold: "
            f"{alchemy.transmutation.recipes.lead_to_gold()}")
    except Exception as e:
        print(f"{e}")
