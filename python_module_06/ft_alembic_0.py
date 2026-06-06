import elements


if __name__ == "__main__":
    try:
        print("=== Alembic 0 ===")
        print("Using: 'import ...' structure to access elements.py")
        print(f"Testing create_fire: {elements.create_fire()}")
    except Exception as e:
        print(f"{e}")
