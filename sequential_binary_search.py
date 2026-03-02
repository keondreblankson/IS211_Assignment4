"""
Week 4 Assignment – Part I: Algorithm Comparison (Searching)

Required functions:
- sequential_search
- ordered_sequential_search
- binary_search_iterative
- binary_search_recursive

Benchmark requirements:
- For each list size, generate 100 separate lists
- Do 10,000 searches total (100 lists * 100 searches each)
- Search for a value not in the list (worst case), e.g., 99999999
- Return (result, time_taken) from each search function
- Print total time and average time in the format:
  "Sequential Search took [time_taken:10.7] seconds to run, on average"
"""

from __future__ import annotations

import random
import time
from typing import List, Tuple

TARGET_NOT_IN_LIST = 99_999_999


def sequential_search(items: List[int], target: int) -> Tuple[int, float]:
    """Linear search on an unsorted list. Returns (index_or_-1, seconds)."""
    start = time.perf_counter()
    for i, val in enumerate(items):
        if val == target:
            end = time.perf_counter()
            return i, end - start
    end = time.perf_counter()
    return -1, end - start


def ordered_sequential_search(items_sorted: List[int], target: int) -> Tuple[int, float]:
    """
    Linear search on a sorted list with early-stop.
    Returns (index_or_-1, seconds).
    """
    start = time.perf_counter()
    for i, val in enumerate(items_sorted):
        if val == target:
            end = time.perf_counter()
            return i, end - start
        if val > target:  # early stop because sorted
            end = time.perf_counter()
            return -1, end - start
    end = time.perf_counter()
    return -1, end - start


def binary_search_iterative(items_sorted: List[int], target: int) -> Tuple[int, float]:
    """Iterative binary search on a sorted list. Returns (index_or_-1, seconds)."""
    start = time.perf_counter()

    low = 0
    high = len(items_sorted) - 1
    while low <= high:
        mid = (low + high) // 2
        guess = items_sorted[mid]
        if guess == target:
            end = time.perf_counter()
            return mid, end - start
        if guess < target:
            low = mid + 1
        else:
            high = mid - 1

    end = time.perf_counter()
    return -1, end - start


def _binary_search_recursive_core(items_sorted: List[int], target: int, low: int, high: int) -> int:
    """Recursive core (no timing). Returns index_or_-1."""
    if low > high:
        return -1
    mid = (low + high) // 2
    guess = items_sorted[mid]
    if guess == target:
        return mid
    if guess < target:
        return _binary_search_recursive_core(items_sorted, target, mid + 1, high)
    return _binary_search_recursive_core(items_sorted, target, low, mid - 1)


def binary_search_recursive(items_sorted: List[int], target: int) -> Tuple[int, float]:
    """Recursive binary search on a sorted list. Returns (index_or_-1, seconds)."""
    start = time.perf_counter()
    idx = _binary_search_recursive_core(items_sorted, target, 0, len(items_sorted) - 1)
    end = time.perf_counter()
    return idx, end - start


def _make_random_list(size: int) -> List[int]:
    # Use a range that will not accidentally include TARGET_NOT_IN_LIST
    return [random.randint(1, 10_000_000) for _ in range(size)]


def _print_avg(label: str, total_seconds: float, runs: int) -> None:
    avg = total_seconds / runs
    # matches assignment-style bracket formatting
    print(f"{label} took [time_taken:{avg:10.7f}] seconds to run, on average")


def benchmark_searches(list_sizes: List[int]) -> None:
    random.seed(211)

    searches_per_list = 100          # 100 searches per list
    number_of_lists = 100            # 100 lists
    total_searches = searches_per_list * number_of_lists  # 10,000

    for size in list_sizes:
        # Build 100 lists (and sorted copies for sorted algorithms)
        lists_unsorted = [_make_random_list(size) for _ in range(number_of_lists)]
        lists_sorted = [sorted(lst) for lst in lists_unsorted]  # sorting time excluded

        total_seq = 0.0
        total_ord = 0.0
        total_bin_it = 0.0
        total_bin_rec = 0.0

        # 10,000 searches total per algorithm
        for i in range(number_of_lists):
            u = lists_unsorted[i]
            s = lists_sorted[i]

            for _ in range(searches_per_list):
                _, t = sequential_search(u, TARGET_NOT_IN_LIST)
                total_seq += t

                _, t = ordered_sequential_search(s, TARGET_NOT_IN_LIST)
                total_ord += t

                _, t = binary_search_iterative(s, TARGET_NOT_IN_LIST)
                total_bin_it += t

                _, t = binary_search_recursive(s, TARGET_NOT_IN_LIST)
                total_bin_rec += t

        print(f"\n--- List size: {size} | Worst-case target: {TARGET_NOT_IN_LIST} | Total searches per algorithm: {total_searches} ---")
        _print_avg("Sequential Search", total_seq, total_searches)
        _print_avg("Ordered Sequential Search", total_ord, total_searches)
        _print_avg("Binary Search (Iterative)", total_bin_it, total_searches)
        _print_avg("Binary Search (Recursive)", total_bin_rec, total_searches)


def main() -> None:
    # If your assignment only lists 500/1000/5000, remove 10000.
    list_sizes = [500, 1_000, 5_000, 10_000]
    benchmark_searches(list_sizes)


if __name__ == "__main__":
    main()
