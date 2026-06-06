import alchemy.elements


if __name__ == "__main__":
    try:
        print("=== Alembic 2 ===")
        print("Accessing alchemy/elements.py using 'import ...' structure")
        print(f"Testing create_earth: {alchemy.elements.create_earth()}")
    except Exception as e:
        print(f"{e}")
