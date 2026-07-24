from typing import Any, Dict
from .base_kernel import BaseKernel

class PythonKernel(BaseKernel):
    """
    A kernel implementation that executes Python code.
    """

    def is_capable(self, instruction_type: str) -> bool:
        return instruction_type == 'python'

    def execute(self, instruction: Any, context: Dict[str, Any]) -> Any:
        """
        Executes Python code.
        
        :param instruction: The Python code to execute (as a string).
        :param context: The current execution context.
        :return: The result of the execution.
        """
        # CAUTION: Using exec() is dangerous. 
        # In a real-world scenario, this should be executed in a sandboxed environment.
        
        local_vars = {}
        # Provide access to hivemind state within the execution
        local_vars['hivemind'] = context.get('hivemind')
        
        try:
            exec(instruction, {}, local_vars)
            # Assuming the last executed expression result might be stored in a variable
            return local_vars.get('result')
        except Exception as e:
            raise Exception(f"Python execution failed: {e}")

    def setup(self) -> None:
        pass

    def teardown(self) -> None:
        pass
