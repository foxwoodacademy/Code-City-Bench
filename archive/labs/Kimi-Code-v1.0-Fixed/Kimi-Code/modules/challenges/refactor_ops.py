"""
Kimi-Code: Refactor Operations
Improve code quality without changing behavior.
"""
from typing import Dict, List

REFACTOR_MISSIONS = [
    {
        "id": "refactor_001",
        "title": "Extract Method",
        "description": "Extract duplicated logic into reusable methods.",
        "before": "def process_order(order):
    if order['type'] == 'digital':
        tax = order['amount'] * 0.0
        total = order['amount'] + tax
        print(f'Digital: {total}')
    elif order['type'] == 'physical':
        tax = order['amount'] * 0.08
        total = order['amount'] + tax
        print(f'Physical: {total}')
    elif order['type'] == 'service':
        tax = order['amount'] * 0.15
        total = order['amount'] + tax
        print(f'Service: {total}')
",
        "after": "TAX_RATES = {'digital': 0.0, 'physical': 0.08, 'service': 0.15}

def calculate_total(amount, order_type):
    tax = amount * TAX_RATES[order_type]
    return amount + tax

def process_order(order):
    total = calculate_total(order['amount'], order['type'])
    print(f'{order["type"].title()}: {total}')
",
        "improvements": ["eliminated_duplication", "single_responsibility", "easier_to_test", "easier_to_modify_tax_rates"],
        "difficulty": 2
    },
    {
        "id": "refactor_002",
        "title": "Replace Conditional with Polymorphism",
        "description": "Convert switch/if-else chains to object-oriented design.",
        "before": "def calculate_salary(employee):
    if employee['type'] == 'hourly':
        return employee['hours'] * employee['rate']
    elif employee['type'] == 'salaried':
        return employee['salary'] / 12
    elif employee['type'] == 'commission':
        return employee['base'] + employee['sales'] * 0.1
",
        "after": "from abc import ABC, abstractmethod

class Employee(ABC):
    @abstractmethod
    def calculate_salary(self):
        pass

class HourlyEmployee(Employee):
    def __init__(self, hours, rate):
        self.hours = hours
        self.rate = rate
    def calculate_salary(self):
        return self.hours * self.rate

class SalariedEmployee(Employee):
    def __init__(self, salary):
        self.salary = salary
    def calculate_salary(self):
        return self.salary / 12

class CommissionEmployee(Employee):
    def __init__(self, base, sales):
        self.base = base
        self.sales = sales
    def calculate_salary(self):
        return self.base + self.sales * 0.1
",
        "improvements": ["open_closed_principle", "extensibility", "type_safety", "testability"],
        "difficulty": 4
    },
    {
        "id": "refactor_003",
        "title": "Introduce Strategy Pattern",
        "description": "Make sorting algorithm interchangeable.",
        "before": "def sort_data(data, algorithm='quick'):
    if algorithm == 'quick':
        return quicksort(data)
    elif algorithm == 'merge':
        return mergesort(data)
    elif algorithm == 'bubble':
        return bubblesort(data)
    else:
        raise ValueError('Unknown algorithm')
",
        "after": "from abc import ABC, abstractmethod
from typing import List

class SortStrategy(ABC):
    @abstractmethod
    def sort(self, data: List) -> List:
        pass

class QuickSort(SortStrategy):
    def sort(self, data: List) -> List:
        if len(data) <= 1:
            return data
        pivot = data[len(data) // 2]
        left = [x for x in data if x < pivot]
        middle = [x for x in data if x == pivot]
        right = [x for x in data if x > pivot]
        return self.sort(left) + middle + self.sort(right)

class MergeSort(SortStrategy):
    def sort(self, data: List) -> List:
        if len(data) <= 1:
            return data
        mid = len(data) // 2
        left = self.sort(data[:mid])
        right = self.sort(data[mid:])
        return self._merge(left, right)
    
    def _merge(self, left, right):
        result = []
        while left and right:
            if left[0] < right[0]:
                result.append(left.pop(0))
            else:
                result.append(right.pop(0))
        result.extend(left or right)
        return result

class Sorter:
    def __init__(self, strategy: SortStrategy):
        self.strategy = strategy
    
    def sort(self, data: List) -> List:
        return self.strategy.sort(data)
    
    def set_strategy(self, strategy: SortStrategy):
        self.strategy = strategy
",
        "improvements": ["interchangeable_algorithms", "runtime_selection", "easy_to_add_new", "separation_of_concerns"],
        "difficulty": 5
    }
]

def get_missions(difficulty_range: tuple = None) -> List[Dict]:
    missions = REFACTOR_MISSIONS
    if difficulty_range:
        min_d, max_d = difficulty_range
        missions = [m for m in missions if min_d <= m["difficulty"] <= max_d]
    return missions
