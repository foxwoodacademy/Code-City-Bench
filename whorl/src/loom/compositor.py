from typing import List, Dict, Any, Optional
from .strategies import CompositionStrategy, AggregateStrategy
from .exceptions import CompositionError

class LoomCompositor:
    """
    The output compositor for the Whorl ecosystem.
    Weaves parallel agent outputs into unified deliverables.
    """
    
    def __init__(self, strategy: Optional[CompositionStrategy] = None):
        self.strategy = strategy or AggregateStrategy()
        
    def set_strategy(self, strategy: CompositionStrategy):
        self.strategy = strategy
        
    def weave(self, agent_outputs: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Composes the outputs from various agents into a unified structure.
        
        :param agent_outputs: A list of dictionaries representing outputs from different agents.
        :return: A unified dictionary representing the composed deliverable.
        """
        try:
            return self.strategy.compose(agent_outputs)
        except Exception as e:
            raise CompositionError(f"Failed to weave agent outputs: {str(e)}")
