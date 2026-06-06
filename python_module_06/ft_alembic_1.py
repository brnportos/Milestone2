from elements import create_water


if __name__ == "__main__":
    try:
        print("=== Alembic 1 ===")
        print("Using: 'from ... import ...' structure to access elements.py")
        print(f"Testing create_water: {create_water()}")
    except Exception as e:
        print(f"{e}")
