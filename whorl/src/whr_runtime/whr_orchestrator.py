import json
from typing import List, Dict, Any
from src.whr_runtime.kernels.base_kernel import BaseKernel
from src.whr_runtime.kernels.python_kernel import PythonKernel 
from src.whr_runtime.kernels.powershell_kernel import PowerShellKernel
from src.whr_runtime.kernels.bash_kernel import BashKernel
from src.whr_runtime.hivemind_manager import HivemindManager

class WhrOrchestrator:
    # ...
    def __init__(self):
        self.hivemind = HivemindManager()
        self.kernels: List[BaseKernel] = [
            PythonKernel(),
            PowerShellKernel(),
            BashKernel()
        ]
# ...


    def _get_kernel(self, instruction_type: str) -> BaseKernel:
        for kernel in self.kernels:
            if kernel.is_capable(instruction_type):
                return kernel
        raise Exception(f"No kernel capable of handling instruction type: {instruction_type}")

    def execute_instruction(self, instruction_type: str, instruction_body: str) -> Any:
        """
        Executes a single instruction. Ensures atomic state synchronization.
        """
        # 1. Atomic Save before handing off to kernel
        self.hivemind.save()
        
        # 2. Dispatch
        kernel = self._get_kernel(instruction_type)
        
        # In a more advanced implementation, context would include the Hivemind state
        context = {"hivemind": self.hivemind}
        
        result = kernel.execute(instruction_body, context)
        
        # 3. Implicit Evaluation: Capture stdout into Hivemind if applicable
        # This is a basic implementation of implicit capture
        if instruction_type == 'powershell':
            self.hivemind.set('last_ps_output', result)
            
        # 4. Atomic Save after execution
        self.hivemind.save()
        
        return result
