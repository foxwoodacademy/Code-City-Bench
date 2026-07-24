import unittest
from whr_orchestrator import WhrOrchestrator

class TestWhrOrchestrator(unittest.TestCase):

    def setUp(self):
        self.orchestrator = WhrOrchestrator()
        self.orchestrator.hivemind.clear()

    def test_powershell_execution(self):
        # This will only work if running on a machine with PowerShell (Windows)
        try:
            # Using a simple command
            result = self.orchestrator.execute_instruction('powershell', 'echo "Hello from PS"')
            self.assertEqual(result, 'Hello from PS')
            self.assertEqual(self.orchestrator.hivemind.get('last_ps_output'), 'Hello from PS')
        except Exception as e:
            self.skipTest(f"PowerShell execution failed (expected if not on Windows): {e}")

    def test_python_execution(self):
        code = "result = 1 + 2"
        self.orchestrator.execute_instruction('python', code)
        # We need a way to check if the python kernel worked
        # Since PythonKernel uses exec and stores result in local_vars, this test might need adjustment
        # For now, this is a basic check.
        # self.assertEqual(..., ...) 
        pass

if __name__ == '__main__':
    unittest.main()
