"""
Kimi-Code: Algorithm Races
Implement and optimize algorithms under time pressure.
"""
from typing import Dict, List

ALGO_RACES = [
    {
        "id": "algo_race_001",
        "title": "Two Sum Speedrun",
        "description": "Find two numbers that add up to target. Optimize from O(n²) to O(n).",
        "starter_code": "def two_sum(nums, target):
    for i in range(len(nums)):
        for j in range(i + 1, len(nums)):
            if nums[i] + nums[j] == target:
                return [i, j]
    return []
",
        "optimized_code": "def two_sum(nums, target):
    seen = {}
    for i, num in enumerate(nums):
        complement = target - num
        if complement in seen:
            return [seen[complement], i]
        seen[num] = i
    return []
",
        "time_improvement": "O(n²) → O(n)",
        "space_tradeoff": "O(1) → O(n)",
        "difficulty": 3
    },
    {
        "id": "algo_race_002",
        "title": "Merge K Sorted Arrays",
        "description": "Efficiently merge k sorted arrays into one.",
        "starter_code": "def merge_k_arrays(arrays):
    result = []
    for arr in arrays:
        result.extend(arr)
    return sorted(result)
",
        "optimized_code": "import heapq

def merge_k_arrays(arrays):
    result = []
    heap = []
    
    for i, arr in enumerate(arrays):
        if arr:
            heapq.heappush(heap, (arr[0], i, 0))
    
    while heap:
        val, arr_idx, elem_idx = heapq.heappop(heap)
        result.append(val)
        
        if elem_idx + 1 < len(arrays[arr_idx]):
            next_val = arrays[arr_idx][elem_idx + 1]
            heapq.heappush(heap, (next_val, arr_idx, elem_idx + 1))
    
    return result
",
        "time_improvement": "O(n*k log(n*k)) → O(n log k)",
        "space_tradeoff": "O(n*k) → O(n + k)",
        "difficulty": 5
    },
    {
        "id": "algo_race_003",
        "title": "Sliding Window Maximum",
        "description": "Find maximum in every window of size k.",
        "starter_code": "def max_sliding_window(nums, k):
    result = []
    for i in range(len(nums) - k + 1):
        result.append(max(nums[i:i+k]))
    return result
",
        "optimized_code": "from collections import deque

def max_sliding_window(nums, k):
    result = []
    dq = deque()
    
    for i, num in enumerate(nums):
        while dq and nums[dq[-1]] <= num:
            dq.pop()
        dq.append(i)
        
        if dq[0] <= i - k:
            dq.popleft()
        
        if i >= k - 1:
            result.append(nums[dq[0]])
    
    return result
",
        "time_improvement": "O(n*k) → O(n)",
        "space_tradeoff": "O(1) → O(k)",
        "difficulty": 6
    }
]

def get_races(difficulty_range: tuple = None) -> List[Dict]:
    races = ALGO_RACES
    if difficulty_range:
        min_d, max_d = difficulty_range
        races = [r for r in races if min_d <= r["difficulty"] <= max_d]
    return races
