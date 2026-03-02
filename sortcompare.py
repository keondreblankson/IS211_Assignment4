"""
Week 4 Assignment – Part II: Sorting Algorithm Comparison

Required functions:
- insertion_sort
- shell_sort
- python_sort
- wrapper (runs the benchmark and prints results)

Benchmark:
- For each list size, generate 100 random lists
- Time each sorting algorithm on identical data (copy the list)
- Print average time in the same format as Part I
"""

from __future__ import annotations

import random
import time
from typing import List

# Import your Part I file (required by assignment)
import sequential_binary_search


def insertion_sort(items: List[int]) -> float:
    """In-place insertion sort. Returns elapsed seconds."""
    start = time.perf_counter()
    for i in range(1, len(items)):
        current = items[i]
        j = i - 1
        while j >= 0 and items[j] > current:
            items[j + 1] = items[j]
            j -= 1
        items[j + 1] = current
    end = time.perf_counter()
    return end - start


def shell_sort(items: List[int]) -> float:
    """In-place shell sort. Returns elapsed seconds."""
    start = time.perf_counter()
    n = len(items)
    gap = n // 2
    while gap > 0:
        for i in range(gap, n):
            temp = items[i]
            j = i
            while j >= gap and items[j - gap] > temp:
                items[j] = items[j - gap]
                j -= gap
            items[j] = temp
        gap //= 2
    end = time.perf_counter()
    return end - start


def python_sort(items: List[int]) -> float:
    """Python built-in sort. Returns elapsed seconds."""
    start = time.perf_counter()
    items.sort()
    end = time.perf_counter()
    return end - start


def _make_random_list(size: int) -> List[int]:
    return [random.randint(1, 10_000_000) for _ in range(size)]


def _print_avg(label: str, total_seconds: float, runs: int) -> None:
    avg = total_seconds / runs
    print(f"{label} took [time_taken:{avg:10.7f}] seconds to run, on average")


def wrapper(list_sizes: List[int]) -> None:
    random.seed(211)

    number_of_lists = 100  # 100 lists per size

    for size in list_sizes:
        total_ins = 0.0
        total_shell = 0.0
        total_py = 0.0

        for _ in range(number_of_lists):
            base = _make_random_list(size)

            a = base.copy()
            b = base.copy()
            c = base.copy()

            total_ins += insertion_sort(a)
            total_shell += shell_sort(b)
            total_py += python_sort(c)

        print(f"\n--- List size: {size} | Total sorts per algorithm: {number_of_lists} ---")
        _print_avg("Insertion Sort", total_ins, number_of_lists)
        _print_avg("Shell Sort", total_shell, number_of_lists)
        _print_avg("Python Built-in Sort", total_py, number_of_lists)


def main() -> None:
    # If your assignment only lists 500/1000/5000, remove 10000.
    list_sizes = [500, 1_000, 5_000, 10_000]
    wrapper(list_sizes)


if __name__ == "__main__":
    main()
