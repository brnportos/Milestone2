from ex0 import FlameFactory, AquaFactory
from ex0.factories import CreatureFactory

def test_factories(factories: CreatureFactory) -> None:
    base = factories.create_base()
    evolved = factories.create_evolved()
    try:
        print("Testing factory")
        print(base.describe())
        print(base.attack())
        print(evolved.describe())
        print(evolved.attack())
        print()
    except Exception as e:
        print(f"{e}")

def test_battle(factories_a: CreatureFactory, factories_b: CreatureFactory) -> None:
    a = factories_a.create_base()
    b = factories_b.create_base()
    try:
        print("\nTesting battle")
        print(f"{a.describe()} \n vs.\n{b.describe()} fight!")
        print(a.attack())
        print(b.attack())
    except Exception as e:
        print(f"{e}")


if __name__ == "__main__":
    try:
        flame_factory = FlameFactory()
        aqua_factory = AquaFactory()
        test_factories(flame_factory)
        test_factories(aqua_factory)
        test_battle(flame_factory, aqua_factory)
    except Exception as e:
        print(f"{e}")
