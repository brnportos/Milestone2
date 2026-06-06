from alchemy import create_air


if __name__ == "__main__":
    try:
        print("=== Alembic 5 ===")
        print("Accessing the alchemy module using 'from alchemy import ...'")
        print(f"Testing create_air: {create_air()}")
    except Exception as e:
        print(f"{e}")
