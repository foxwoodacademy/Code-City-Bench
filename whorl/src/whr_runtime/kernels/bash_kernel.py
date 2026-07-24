import subprocess
from typing import Any, Dict
from .base_kernel import BaseKernel

class BashKernel(BaseKernel):
    """
    A kernel implementation that executes Bash commands.
    """

    def is_capable(self, instruction_type: str) -> bool:
        return instruction_type == 'bash'

    def execute(self, instruction: str, context: Dict[str, Any]) -> Any:
        try:
            result = subprocess.run(
                ['bash', '-c', instruction],
                capture_output=True,
                text=True,
                check=True
            )
            return result.stdout.strip()
        except subprocess.CalledProcessError as e:
            error_msg = f"Bash execution failed: {e.stderr.strip()}"
            raise Exception(error_msg)

    def setup(self) -> None:
        pass

    def teardown(self) -> None:
        pass
