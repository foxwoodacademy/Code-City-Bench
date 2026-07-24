"""
Kimi-Code: Python Track
Progressive challenges from basics to metaprogramming.
"""
from typing import List, Dict

PYTHON_CHALLENGES = {
    "basics": [
        {
            "id": "py_basics_001",
            "title": "Variable Detective",
            "description": "Fix variable naming, add type hints, and add a proper docstring.",
            "starter_code": "def calc(x, y, z):
    a = x + y
    b = a * z
    return b
",
            "solution": "def calculate_total(base_value: int, multiplier: int, tax_rate: float) -> float:
    """Calculate total cost including tax."""
    subtotal = base_value * multiplier
    total = subtotal * (1 + tax_rate)
    return total
",
            "test_cases": [
                {"input": "calculate_total(10, 2, 0.1)", "expected": "22.0"},
                {"input": "calculate_total(0, 5, 0.2)", "expected": "0.0"}
            ],
            "hints": [
                "Use descriptive names that explain what the variable represents",
                "Type hints go after the parameter name with a colon",
                "Docstrings use triple quotes right after the function definition"
            ],
            "concepts": ["naming", "type_hints", "docstrings"],
            "difficulty": 1
        },
        {
            "id": "py_basics_002",
            "title": "List Comprehension Master",
            "description": "Refactor this loop into a single list comprehension.",
            "starter_code": "result = []
for i in range(100):
    if i % 2 == 0:
        result.append(i * 2)
",
            "solution": "result = [i * 2 for i in range(100) if i % 2 == 0]
",
            "test_cases": [
                {"input": "len(result)", "expected": "50"},
                {"input": "result[0]", "expected": "0"},
                {"input": "result[-1]", "expected": "196"}
            ],
            "hints": [
                "The format is [expression for item in iterable if condition]",
                "Move the append expression to the front",
                "The filter condition goes at the end"
            ],
            "concepts": ["list_comprehension", "refactoring"],
            "difficulty": 2
        },
        {
            "id": "py_basics_003",
            "title": "Dictionary Deep Dive",
            "description": "Implement a nested dictionary merge with conflict resolution. Last value wins.",
            "starter_code": "def merge_dicts(d1: dict, d2: dict) -> dict:
    # TODO: Implement deep merge
    pass
",
            "solution": "def merge_dicts(d1: dict, d2: dict) -> dict:
    """Deep merge two dictionaries. d2 values take precedence."""
    result = d1.copy()
    for key, value in d2.items():
        if key in result and isinstance(result[key], dict) and isinstance(value, dict):
            result[key] = merge_dicts(result[key], value)
        else:
            result[key] = value
    return result
",
            "test_cases": [
                {"input": "merge_dicts({'a': 1}, {'b': 2})", "expected": "{'a': 1, 'b': 2}"},
                {"input": "merge_dicts({'a': {'x': 1}}, {'a': {'y': 2}})", "expected": "{'a': {'x': 1, 'y': 2}}"}
            ],
            "hints": [
                "Recursively merge when both values are dictionaries",
                "Use .copy() to avoid mutating the original",
                "Handle the base case where keys don't overlap"
            ],
            "concepts": ["recursion", "dictionaries", "deep_merge"],
            "difficulty": 3
        },
        {
            "id": "py_basics_004",
            "title": "Error Handling Essentials",
            "description": "Add proper exception handling to this file reader.",
            "starter_code": "def read_config(path):
    with open(path) as f:
        return json.load(f)
",
            "solution": "def read_config(path: str) -> dict:
    """Safely read and parse a JSON config file."""
    try:
        with open(path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        raise ValueError(f'Config file not found: {path}')
    except json.JSONDecodeError as e:
        raise ValueError(f'Invalid JSON in {path}: {e}')
    except PermissionError:
        raise ValueError(f'Permission denied: {path}')
",
            "test_cases": [
                {"input": "read_config('test.json')", "expected": "dict"},
                {"input": "read_config('nonexistent.json')", "expected": "ValueError"}
            ],
            "hints": [
                "Catch specific exceptions, not bare except:",
                "Always provide meaningful error messages",
                "Consider encoding issues with file I/O"
            ],
            "concepts": ["exception_handling", "file_io", "json"],
            "difficulty": 2
        }
    ],
    "data_structures": [
        {
            "id": "py_ds_001",
            "title": "Custom Stack with Min Tracking",
            "description": "Implement a stack that supports O(1) push, pop, and get_min operations.",
            "starter_code": "class MinStack:
    def __init__(self):
        pass
    def push(self, val: int) -> None:
        pass
    def pop(self) -> None:
        pass
    def top(self) -> int:
        pass
    def get_min(self) -> int:
        pass
",
            "solution": "class MinStack:
    """Stack with O(1) min tracking using auxiliary stack."""
    def __init__(self):
        self.stack = []
        self.min_stack = []
    
    def push(self, val: int) -> None:
        self.stack.append(val)
        if not self.min_stack or val <= self.min_stack[-1]:
            self.min_stack.append(val)
    
    def pop(self) -> None:
        val = self.stack.pop()
        if val == self.min_stack[-1]:
            self.min_stack.pop()
    
    def top(self) -> int:
        return self.stack[-1]
    
    def get_min(self) -> int:
        return self.min_stack[-1]
",
            "test_cases": [
                {"input": "s=MinStack();s.push(-2);s.push(0);s.push(-3);s.get_min()", "expected": "-3"},
                {"input": "s.pop();s.top()", "expected": "0"},
                {"input": "s.get_min()", "expected": "-2"}
            ],
            "hints": [
                "Use a second stack to track minimums",
                "Only push to min_stack when value <= current min",
                "Pop from min_stack when popped value equals current min"
            ],
            "concepts": ["stack", "auxiliary_data_structure", "O1_operations"],
            "difficulty": 4
        },
        {
            "id": "py_ds_002",
            "title": "LRU Cache Implementation",
            "description": "Implement an LRU Cache with O(1) get and put operations.",
            "starter_code": "class LRUCache:
    def __init__(self, capacity: int):
        self.capacity = capacity
    def get(self, key: int) -> int:
        pass
    def put(self, key: int, value: int) -> None:
        pass
",
            "solution": "from collections import OrderedDict

class LRUCache:
    """LRU Cache using OrderedDict for O(1) operations."""
    def __init__(self, capacity: int):
        self.capacity = capacity
        self.cache = OrderedDict()
    
    def get(self, key: int) -> int:
        if key not in self.cache:
            return -1
        self.cache.move_to_end(key)
        return self.cache[key]
    
    def put(self, key: int, value: int) -> None:
        if key in self.cache:
            self.cache.move_to_end(key)
        self.cache[key] = value
        if len(self.cache) > self.capacity:
            self.cache.popitem(last=False)
",
            "test_cases": [
                {"input": "c=LRUCache(2);c.put(1,1);c.put(2,2);c.get(1)", "expected": "1"},
                {"input": "c.put(3,3);c.get(2)", "expected": "-1"}
            ],
            "hints": [
                "OrderedDict maintains insertion order and supports move_to_end",
                "On get, move accessed item to end (most recently used)",
                "On eviction, pop from front (least recently used)"
            ],
            "concepts": ["lru_cache", "ordered_dict", "cache_eviction"],
            "difficulty": 5
        },
        {
            "id": "py_ds_003",
            "title": "Trie for Autocomplete",
            "description": "Implement a Trie data structure with insert, search, and startsWith methods.",
            "starter_code": "class TrieNode:
    def __init__(self):
        pass

class Trie:
    def __init__(self):
        pass
    def insert(self, word: str) -> None:
        pass
    def search(self, word: str) -> bool:
        pass
    def startsWith(self, prefix: str) -> bool:
        pass
",
            "solution": "class TrieNode:
    def __init__(self):
        self.children = {}
        self.is_end = False

class Trie:
    def __init__(self):
        self.root = TrieNode()
    
    def insert(self, word: str) -> None:
        node = self.root
        for char in word:
            if char not in node.children:
                node.children[char] = TrieNode()
            node = node.children[char]
        node.is_end = True
    
    def search(self, word: str) -> bool:
        node = self._traverse(word)
        return node is not None and node.is_end
    
    def startsWith(self, prefix: str) -> bool:
        return self._traverse(prefix) is not None
    
    def _traverse(self, word: str):
        node = self.root
        for char in word:
            if char not in node.children:
                return None
            node = node.children[char]
        return node
",
            "test_cases": [
                {"input": "t=Trie();t.insert('apple');t.search('apple')", "expected": "True"},
                {"input": "t.search('app')", "expected": "False"},
                {"input": "t.startsWith('app')", "expected": "True"}
            ],
            "hints": [
                "Each node represents a character and has children dict",
                "is_end marks the end of a complete word",
                "Traverse character by character, creating nodes as needed"
            ],
            "concepts": ["trie", "prefix_tree", "autocomplete"],
            "difficulty": 5
        }
    ],
    "algorithms": [
        {
            "id": "py_algo_001",
            "title": "Binary Search Variants",
            "description": "Implement lower_bound (first index >= target) and upper_bound (first index > target).",
            "starter_code": "from typing import List

def lower_bound(arr: List[int], target: int) -> int:
    """First index where arr[i] >= target"""
    pass

def upper_bound(arr: List[int], target: int) -> int:
    """First index where arr[i] > target"""
    pass
",
            "solution": "from typing import List

def lower_bound(arr: List[int], target: int) -> int:
    left, right = 0, len(arr)
    while left < right:
        mid = (left + right) // 2
        if arr[mid] < target:
            left = mid + 1
        else:
            right = mid
    return left

def upper_bound(arr: List[int], target: int) -> int:
    left, right = 0, len(arr)
    while left < right:
        mid = (left + right) // 2
        if arr[mid] <= target:
            left = mid + 1
        else:
            right = mid
    return left
",
            "test_cases": [
                {"input": "lower_bound([1,2,2,3,4], 2)", "expected": "1"},
                {"input": "upper_bound([1,2,2,3,4], 2)", "expected": "3"},
                {"input": "lower_bound([1,3,5], 0)", "expected": "0"}
            ],
            "hints": [
                "Use half-open interval [left, right)",
                "For lower_bound: move left when arr[mid] < target",
                "For upper_bound: move left when arr[mid] <= target"
            ],
            "concepts": ["binary_search", "bounds", "sorted_arrays"],
            "difficulty": 5
        },
        {
            "id": "py_algo_002",
            "title": "Climbing Stairs - DP",
            "description": "Count ways to climb n stairs taking 1 or 2 steps at a time. Use memoization.",
            "starter_code": "def climb_stairs(n: int) -> int:
    """Count distinct ways to climb n stairs."""
    pass
",
            "solution": "from functools import lru_cache

def climb_stairs(n: int) -> int:
    """Count distinct ways to climb n stairs (1 or 2 steps)."""
    @lru_cache(maxsize=None)
    def dp(i: int) -> int:
        if i <= 1:
            return 1
        return dp(i - 1) + dp(i - 2)
    return dp(n)
",
            "test_cases": [
                {"input": "climb_stairs(2)", "expected": "2"},
                {"input": "climb_stairs(3)", "expected": "3"},
                {"input": "climb_stairs(4)", "expected": "5"}
            ],
            "hints": [
                "At each step, you can come from n-1 or n-2",
                "Base cases: 0 stairs = 1 way, 1 stair = 1 way",
                "Use memoization to avoid recomputation"
            ],
            "concepts": ["dynamic_programming", "memoization", "fibonacci"],
            "difficulty": 4
        },
        {
            "id": "py_algo_003",
            "title": "Dijkstra's Shortest Path",
            "description": "Implement Dijkstra's algorithm to find shortest paths from a source node.",
            "starter_code": "import heapq
from typing import Dict, List, Tuple

def dijkstra(graph: Dict[int, List[Tuple[int, int]]], start: int) -> Dict[int, int]:
    """Find shortest distances from start to all nodes."""
    pass
",
            "solution": "import heapq
from typing import Dict, List, Tuple

def dijkstra(graph: Dict[int, List[Tuple[int, int]]], start: int) -> Dict[int, int]:
    """Dijkstra's algorithm using min-heap. Returns shortest distances."""
    distances = {node: float('inf') for node in graph}
    distances[start] = 0
    pq = [(0, start)]
    
    while pq:
        dist, node = heapq.heappop(pq)
        if dist > distances[node]:
            continue
        for neighbor, weight in graph[node]:
            new_dist = dist + weight
            if new_dist < distances[neighbor]:
                distances[neighbor] = new_dist
                heapq.heappush(pq, (new_dist, neighbor))
    
    return distances
",
            "test_cases": [
                {"input": "g={0:[(1,4),(2,1)],1:[(3,1)],2:[(1,2),(3,5)],3:[]};dijkstra(g,0)", "expected": "{0:0,1:3,2:1,3:4}"},
            ],
            "hints": [
                "Use a priority queue (min-heap) ordered by distance",
                "Skip processing if we've already found a shorter path",
                "Relax edges: if new_dist < current_dist, update and push to heap"
            ],
            "concepts": ["dijkstra", "shortest_path", "priority_queue", "graph"],
            "difficulty": 7
        }
    ],
    "oop": [
        {
            "id": "py_oop_001",
            "title": "Bank Account with Transactions",
            "description": "Design a thread-safe bank account with deposit, withdraw, and transaction history.",
            "starter_code": "from threading import Lock
from dataclasses import dataclass
from typing import List
from datetime import datetime

@dataclass
class Transaction:
    amount: float
    timestamp: datetime
    type: str

class BankAccount:
    def __init__(self, account_id: str):
        pass
    def deposit(self, amount: float) -> None:
        pass
    def withdraw(self, amount: float) -> bool:
        pass
    def get_balance(self) -> float:
        pass
    def get_history(self) -> List[Transaction]:
        pass
",
            "solution": "from threading import Lock
from dataclasses import dataclass
from typing import List
from datetime import datetime

@dataclass
class Transaction:
    amount: float
    timestamp: datetime
    type: str

class BankAccount:
    """Thread-safe bank account with transaction history."""
    def __init__(self, account_id: str):
        self.account_id = account_id
        self._balance = 0.0
        self._history: List[Transaction] = []
        self._lock = Lock()
    
    def deposit(self, amount: float) -> None:
        if amount <= 0:
            raise ValueError('Deposit amount must be positive')
        with self._lock:
            self._balance += amount
            self._history.append(Transaction(amount, datetime.now(), 'deposit'))
    
    def withdraw(self, amount: float) -> bool:
        if amount <= 0:
            raise ValueError('Withdrawal amount must be positive')
        with self._lock:
            if amount > self._balance:
                return False
            self._balance -= amount
            self._history.append(Transaction(-amount, datetime.now(), 'withdrawal'))
            return True
    
    def get_balance(self) -> float:
        with self._lock:
            return self._balance
    
    def get_history(self) -> List[Transaction]:
        with self._lock:
            return self._history.copy()
",
            "test_cases": [
                {"input": "acc=BankAccount('123');acc.deposit(100);acc.get_balance()", "expected": "100.0"},
                {"input": "acc.withdraw(50);acc.get_balance()", "expected": "50.0"},
                {"input": "acc.withdraw(100)", "expected": "False"}
            ],
            "hints": [
                "Use threading.Lock for thread safety",
                "Validate all inputs before processing",
                "Return copies of mutable state (history)"
            ],
            "concepts": ["oop", "threading", "encapsulation", "dataclasses"],
            "difficulty": 5
        }
    ],
    "async": [
        {
            "id": "py_async_001",
            "title": "Async Task Queue with Priority",
            "description": "Implement a priority task queue using asyncio.",
            "starter_code": "import asyncio
from typing import Callable, Any
from dataclasses import dataclass, field

@dataclass(order=True)
class Task:
    priority: int
    coro: Callable = field(compare=False)

class TaskQueue:
    def __init__(self):
        pass
    async def add_task(self, coro: Callable, priority: int = 0) -> None:
        pass
    async def run(self) -> list:
        pass
",
            "solution": "import asyncio
from typing import Callable, Any, List
from dataclasses import dataclass, field
import heapq

@dataclass(order=True)
class Task:
    priority: int
    seq: int = field(compare=True)
    coro: Callable = field(compare=False)

class TaskQueue:
    """Priority task queue with asyncio. Lower priority = run first."""
    def __init__(self):
        self._queue = []
        self._counter = 0
        self._results = []
    
    async def add_task(self, coro: Callable, priority: int = 0) -> None:
        self._counter += 1
        heapq.heappush(self._queue, Task(priority, self._counter, coro))
    
    async def run(self) -> List[Any]:
        self._results = []
        while self._queue:
            task = heapq.heappop(self._queue)
            try:
                result = await task.coro()
                self._results.append(result)
            except Exception as e:
                self._results.append(f'Error: {e}')
        return self._results
",
            "test_cases": [
                {"input": "async def t1():return 1;async def t2():return 2;q=TaskQueue();await q.add_task(t2(),1);await q.add_task(t1(),0);await q.run()", "expected": "[1, 2]"}
            ],
            "hints": [
                "Use heapq for O(log n) priority operations",
                "Add a sequence counter to break ties deterministically",
                "Await each coroutine and collect results"
            ],
            "concepts": ["asyncio", "priority_queue", "heapq", "coroutines"],
            "difficulty": 7
        }
    ],
    "metaprogramming": [
        {
            "id": "py_meta_001",
            "title": "Decorator with Retry Logic",
            "description": "Create a decorator that retries a function on failure with exponential backoff.",
            "starter_code": "import time
from functools import wraps
from typing import Callable, Type

def retry(max_attempts: int = 3, exceptions: Type[Exception] = Exception,
          delay: float = 1.0, backoff: float = 2.0):
    """Decorator with exponential backoff retry."""
    pass
",
            "solution": "import time
from functools import wraps
from typing import Callable, Type, Tuple

def retry(max_attempts: int = 3, exceptions: Tuple[Type[Exception], ...] = (Exception,),
          delay: float = 1.0, backoff: float = 2.0):
    """Decorator with exponential backoff retry."""
    def decorator(func: Callable):
        @wraps(func)
        def wrapper(*args, **kwargs):
            current_delay = delay
            for attempt in range(1, max_attempts + 1):
                try:
                    return func(*args, **kwargs)
                except exceptions as e:
                    if attempt == max_attempts:
                        raise
                    time.sleep(current_delay)
                    current_delay *= backoff
            return None
        return wrapper
    return decorator
",
            "test_cases": [
                {"input": "@retry(max_attempts=3, delay=0.1)
def flaky():
    flaky.calls = getattr(flaky, 'calls', 0) + 1
    if flaky.calls < 3:
        raise ValueError('fail')
    return 'success'
flaky()", "expected": "'success'"}
            ],
            "hints": [
                "Use functools.wraps to preserve function metadata",
                "Accept exception types as a tuple for flexibility",
                "Multiply delay by backoff after each failure"
            ],
            "concepts": ["decorators", "metaprogramming", "retry_logic", "exponential_backoff"],
            "difficulty": 6
        }
    ]
}

def get_challenges(track: str, difficulty_range: tuple = None) -> List[Dict]:
    """Get challenges for a specific track."""
    challenges = PYTHON_CHALLENGES.get(track, [])
    if difficulty_range:
        min_d, max_d = difficulty_range
        challenges = [c for c in challenges if min_d <= c["difficulty"] <= max_d]
    return challenges

def get_all_tracks() -> List[str]:
    return list(PYTHON_CHALLENGES.keys())

def get_challenge_by_id(challenge_id: str) -> Dict:
    for track in PYTHON_CHALLENGES.values():
        for challenge in track:
            if challenge["id"] == challenge_id:
                return challenge
    return None
