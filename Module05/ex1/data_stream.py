#!/usr/bin/env python3

from abc import ABC, abstractmethod
from typing import Any


class DataProcessor(ABC):
    def __init__(self) -> None:
        self._storage: list[str] = []
        self._current_rank: int = 0

    @abstractmethod
    def validate(self, data: Any) -> bool:
        pass

    @abstractmethod
    def ingest(self, data: Any) -> None:
        pass

    def output(self) -> tuple[int, str]:
        item = self._storage.pop(0)
        rank = self._current_rank
        self._current_rank += 1
        return rank, item

    @property
    def remaining_count(self) -> int:
        return len(self._storage)


class NumericProcessor(DataProcessor):
    def validate(self, data: Any) -> bool:
        if (
            (isinstance(data, (int, float)) and not isinstance(data, bool))
            or
            (
                isinstance(data, list)
                and all(isinstance(i, (int, float)) for i in data))
        ):
            return True
        else:
            return False

    def ingest(self, data: Any) -> None:
        if not self.validate(data):
            raise ValueError("Improper numeric data")
        if isinstance(data, list):
            for item in data:
                self._storage.append(str(item))
        else:
            self._storage.append(str(data))


class TextProcessor(DataProcessor):
    def validate(self, data: Any) -> bool:
        if isinstance(data, str):
            return True
        if isinstance(data, list) and all(isinstance(x, str) for x in data):
            return True
        return False

    def ingest(self, data: Any) -> None:
        if not self.validate(data):
            raise TypeError("Improper text data")
        if isinstance(data, list):
            for item in data:
                self._storage.append(item)
        else:
            self._storage.append(data)


class LogProcessor(DataProcessor):
    def validate(self, data: Any) -> bool:
        if isinstance(data, dict):
            return all(
                isinstance(i, str)
                and isinstance(j, str)
                for i, j in data.items()
                )
        if isinstance(data, list):
            return all(
                isinstance(item, dict) and all(
                    isinstance(i, str)
                    and isinstance(j, str)
                    for i, j in item.items()) for item in data
            )
        return False

    def ingest(self, data: Any) -> None:
        if not self.validate(data):
            raise TypeError("Improper log data")
        entries = data if isinstance(data, list) else [data]
        for entry in entries:
            level = entry.get("log_level", "")
            msg = entry.get("log_message", "")
            self._storage.append(f"{level}: {msg}")


class DataStream:
    def __init__(self) -> None:
        self._processors: list[DataProcessor] = []
        self._stats: dict[DataProcessor, int] = {}

    def register_processor(self, proc: DataProcessor) -> None:
        if proc not in self._processors:
            self._processors.append(proc)
            self._stats[proc] = 0

    def process_stream(self, stream: list[Any]) -> None:
        for element in stream:
            handled = False
            for processor in self._processors:
                if processor.validate(element):
                    processor.ingest(element)
                    increment = (
                        len(element) if isinstance(element, list) else 1
                    )
                    self._stats[processor] += increment
                    handled = True
                    break
            if not handled:
                print(
                    f"DataStream error - Can't process "
                    f"element in stream: {element}"
                    )

    def print_processors_stats(self) -> None:
        print("== DataStream statistics ==")
        if not self._processors:
            print("No processor found, no data")
            return
        for proc in self._processors:
            name = proc.__class__.__name__.replace("Processor", " Processor")
            total = self._stats[proc]
            remaining = proc.remaining_count
            print(
                f"{name}: total {total} items processed, "
                f"remaining {remaining} on processor"
                )


if __name__ == "__main__":
    print("=== Code Nexus - Data Stream ===")
    print("\nInitialize Data Stream...")

    ds = DataStream()
    ds.print_processors_stats()

    print("\nRegistering Numeric Processor\n")
    np = NumericProcessor()
    ds.register_processor(np)
    batch = [
        "Hello world",
        [3.14, -1, 2.71],
        [{
            "log_level": "WARNING",
            "log_message": "Telnet access! Use ssh instead"
            },
         {"log_level": "INFO",    "log_message": "User wil is connected"}],
        42,
        ["Hi", "five"],
    ]

    print(f"Send first batch of data on stream: {batch}")
    ds.process_stream(batch)
    ds.print_processors_stats()
    print("\nRegistering other data processors")
    tp = TextProcessor()
    lp = LogProcessor()
    ds.register_processor(tp)
    ds.register_processor(lp)

    print("Send the same batch again")
    ds.process_stream(batch)
    ds.print_processors_stats()
    print(
        "\nConsume some elements from the data processors: "
        "Numeric 3, Text 2, Log 1"
        )
    for _ in range(3):
        np.output()
    for _ in range(2):
        tp.output()
    for _ in range(1):
        lp.output()
    ds.print_processors_stats()
