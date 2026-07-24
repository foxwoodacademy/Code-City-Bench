from abc import ABC, abstractmethod
from typing import List, Dict, Any

class CompositionStrategy(ABC):
    """Abstract base class for composition strategies."""
    
    @abstractmethod
    def compose(self, inputs: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Composes inputs into a unified result."""
        pass

class AggregateStrategy(CompositionStrategy):
    """Simply aggregates all inputs into a single dictionary."""
    
    def compose(self, inputs: List[Dict[str, Any]]) -> Dict[str, Any]:
        result = {}
        for i, item in enumerate(inputs):
            result[f"item_{i}"] = item
        return result

class SummaryStrategy(CompositionStrategy):
    """Aggregates and attempts a simple summary."""
    
    def compose(self, inputs: List[Dict[str, Any]]) -> Dict[str, Any]:
        summary = {"combined_data": []}
        for item in inputs:
            summary["combined_data"].append(item)
        summary["note"] = "Aggregated by SummaryStrategy"
        return summary
