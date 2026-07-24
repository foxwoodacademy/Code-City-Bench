from abc import ABC, abstractmethod
from typing import Any, Dict

class BaseKernel(ABC):
    """
    Abstract Base Class for all Whorl kernels.
    Defines the interface that every kernel must implement to be managed by the Orchestrator.
    """

    @abstractmethod
    def is_capable(self, instruction_type: str) -> bool:
        """
        Determs if this kernel is capable of handling a specific type of instruction.

        :param instruction_type: The type of instruction (e.g., 'math', 'system', 'agentic').
        :return: True if capable, False otherwise.
        """
        pass

    @abstractmethod
    def execute(self, instruction: Any, context: Dict[str, Any]) -> Any:
        """
        Executes a specific instruction using the kernel's capabilities.

        :param instruction: The instruction data (parsed from the .whr file).
        :param context: The current execution context, including access to the Hivemind state.
        :return: The result of the execution.
        :raises Exception: If execution fails.
        """
        pass

    def setup(self) -> None:
        """
        Optional: Performs any necessary setup before the kernel starts accepting instructions.
        """
        pass

    def teardown(self) -> None:
        """
        Optional: Performs any necessary cleanup after the kernel has finished its work.
        """
        pass
