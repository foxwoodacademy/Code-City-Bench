import subprocess
from typing import Any, Dict
from .base_kernel import BaseKernel

class PowerShellKernel(BaseKernel):
    """
    A kernel implementation that executes PowerShell commands.
    """

    def is_capable(self, instruction_type: str) -> bool:
        return instruction_type == 'powershell'

    def execute(self, instruction: str, context: Dict[str, Any]) -> Any:
        """
        Executes a PowerShell command using subprocess.
        
        :param instruction: The PowerShell command string.
        :param context: The current execution context, including access to Hivemind state.
        :return: The captured output (stdout).
        """
        # Note: In a real-world scenario, we might want to pass context variables 
        # as environment variables to the PowerShell process.
        
        try:
            # We use powershell -Command to execute the instruction.
            # We capture stdout and stderr.
            result = subprocess.run(
                ['powershell', '-Command', instruction],
                capture_output=True,
                text=True,
                check=True
            )
            return result.stdout.strip()
        except subprocess.CalledProcessError as e:
            # Handle PowerShell execution errors gracefully.
            # We might want to raise a specific TransformationError or similar.
            error_msg = f"PowerShell execution failed: {e.stderr.strip()}"
            print(error_msg)
            raise Exception(error_msg)
        except FileNotFoundError:
            raise Exception("PowerShell executable not found. Ensure it is installed and in PATH.")

    def setup(self) -> None:
        # Perform any necessary setup for PowerShell
        pass

    def teardown(self) -> None:
        # Perform any necessary cleanup for PowerShell
        pass
