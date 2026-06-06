import alchemy.transmutation.recipes


if __name__ == "__main__":
    try:
        print("=== Transmutation 0 ===")
        print("Using file alchemy/transmutation/recipes.py directly")
        print(
            f"Testing lead to gold: "
            f"{alchemy.transmutation.recipes.lead_to_gold()}"
            )
    except Exception as e:
        print(f"{e}")
