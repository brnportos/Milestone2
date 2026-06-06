from .creature import Creature

class Aquabub(Creature):
    def __init__(self):
        super().__init__("Aquabub", "Water")

    def attack(self):
        return (f"{self._name} uses Water Gun!")


class Torragon(Creature):
    def __init__(self):
        super().__init__("Torragon", "Water")

    def attack(self):
        return (f"{self._name} uses Hydro Pump!")
