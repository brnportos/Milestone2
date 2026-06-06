from alchemy.elements import create_air


if __name__ == "__main__":
    try:
        print("=== Alembic 3 ===")
        print(
            "Accessing alchemy/elements.py"
            "using 'from ... import ...' structure"
            )
        print(f"Testing create_air: {create_air()}")
    except Exception as e:
        print(f"{e}")
