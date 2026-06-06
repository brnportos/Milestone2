from .creature import Creature

class Flameling(Creature):
    def __init__(self):
        super().__init__("Flameling", " Fire")

    def attack(self):
        return (f"{self._name} uses Ember!")


class Pyrodon(Creature):
    def __init__(self):
        super().__init__("Pyrodon", "Fire/Flying")

    def attack(self):
        return (f"{self._name} uses Flamethrower!")
