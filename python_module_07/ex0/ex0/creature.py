from abc import ABC, abstractmethod

class Creature(ABC):
    def __init__(self, name, typ) -> None:
        self._name = name
        self._typ = typ

    @abstractmethod
    def attack(self) -> str:
        pass

    def describe(self) -> str:
        return (f"{self._name} is a {self._typ} type Creature")
