#!/usr/bin/env python3

from abc import ABC, abstractmethod
from typing import Any, Protocol


class DataProcessor(ABC):
    def __init__(self) -> None:
        self._storage: list[str] = []
        self._total: int = 0
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

    def total_processed(self) -> int:
        return self._total

    def remaining(self) -> int:
        return len(self._storage)

    def record(self, count: int = 1) -> None:
        self._total += count

    def name(self) -> str:
        return self.__class__.__name__


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
                self.record(len(data))
        else:
            self._storage.append(str(data))
            self.record(1)


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
                self.record(len(data))
        else:
            self._storage.append(data)
            self.record(1)


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
        self.record(len(entries))


class ExportPlugin(Protocol):
    def process_output(self, data: list[tuple[int, str]]) -> None:
        pass


class CsvExportPlugin:
    def process_output(self, data: list[tuple[int, str]]) -> None:
        if not data:
            return
        line = ",".join(value for _, value in data)
        print("CSV Output:")
        print(line)


class JsonExportPlugin:
    def process_output(self, data: list[tuple[int, str]]) -> None:
        if not data:
            return
        pairs = ", ".join(f'"item_{rank}": "{value}"' for rank, value in data)
        print("JSON Output:")
        print("{" + pairs + "}")


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

    def output_pipeline(self, nb: int, plugin: ExportPlugin) -> None:
        for processor in self._processors:
            batch: list[tuple[int, str]] = []
            for _ in range(nb):
                if processor.remaining() == 0:
                    break
                batch.append(processor.output())
            if batch:
                plugin.process_output(batch)

    def print_processors_stats(self) -> None:
        print("\n== DataStream statistics ==")
        if not self._processors:
            print("No processor found, no data")
            return
        for proc in self._processors:
            name = proc.__class__.__name__.replace("Processor", " Processor")
            total = self._stats[proc]
            remaining = proc.remaining()
            print(
                f"{name}: total {total} items processed, "
                f"remaining {remaining} on processor"
                )


if __name__ == "__main__":
    print("=== Code Nexus - Data Pipeline ===")
    print("\nInitialize Data Stream...")

    ds = DataStream()
    ds.print_processors_stats()

    print("\nRegistering Processors")
    ds.register_processor(NumericProcessor())
    ds.register_processor(TextProcessor())
    ds.register_processor(LogProcessor())

    batch1 = [
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
    print(f"\nSend first batch of data on stream: {batch1}")
    ds.process_stream(batch1)
    ds.print_processors_stats()

    print("\nSend 3 processed data from each processor to a CSV plugin:")
    ds.output_pipeline(3, CsvExportPlugin())
    ds.print_processors_stats()

    batch2 = [
        21,
        ["I love AI", "LLMs are wonderful", "Stay healthy"],
        [{"log_level": "ERROR",  "log_message": "500 server crash"},
         {
            "log_level": "NOTICE",
            "log_message": "Certificate expires in 10 days"
            }],
        [32, 42, 64, 84, 128, 168],
        "World hello",
    ]
    print(f"\nSend another batch of data: {batch2}")
    ds.process_stream(batch2)
    ds.print_processors_stats()

    print("\nSend 5 processed data from each processor to a JSON plugin:")
    ds.output_pipeline(5, JsonExportPlugin())
    ds.print_processors_stats()
