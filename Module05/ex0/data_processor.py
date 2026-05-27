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


if __name__ == "__main__":
    print("=== Code Nexus - Data Processor ===\n")
    print("Testing Numeric Processor...")

    num_proc = NumericProcessor()
    print(f" Trying to validate input '42': {num_proc.validate(42)}")
    print(f" Trying to validate input 'Hello': {num_proc.validate('Hello')}")
    print(" Test invalid ingestion of string 'foo' without prior validation:")
    try:
        num_proc.ingest("foo")
    except ValueError as e:
        print(f" Got exception: {e}")

    data_num = [1, 2, 3, 4, 5]
    print(f" Processing data: {data_num}")
    num_proc.ingest(data_num)
    print(" Extracting 3 values...")
    for _ in range(3):
        rank, value = num_proc.output()
        print(f" Numeric value {rank}: {value}")

    print("\nTesting Text Processor...")
    text_proc = TextProcessor()
    print(f" Trying to validate input '42': {text_proc.validate(42)}")
    data_txt = ["Hello", "Nexus", "World"]
    print(f" Processing data: {data_txt}")
    text_proc.ingest(data_txt)
    print(" Extracting 1 value...")
    rank, value = text_proc.output()
    print(f" Text value {rank}: {value}")

    print("\nTesting Log Processor...")
    log_proc = LogProcessor()
    print(f" Trying to validate input 'Hello': {log_proc.validate('Hello')}")
    data_log = [
        {"log_level": "NOTICE", "log_message": "Connection to server"},
        {"log_level": "ERROR",  "log_message": "Unauthorized access!!"},
    ]
    print(f" Processing data: {data_log}")
    log_proc.ingest(data_log)
    print(" Extracting 2 values...")
    for _ in range(2):
        rank, value = log_proc.output()
        print(f" Log entry {rank}: {value}")
