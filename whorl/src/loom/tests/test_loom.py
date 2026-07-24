import unittest
from loom.compositor import LoomCompositor
from loom.strategies import SummaryStrategy

class TestLoom(unittest.TestCase):
    
    def setUp(self):
        self.compositor = LoomCompositor()
        self.agent_outputs = [
            {"agent": "Firefly", "result": "scan_complete"},
            {"agent": "Veritas", "result": "validation_passed"}
        ]
        
    def test_aggregate_strategy(self):
        result = self.compositor.weave(self.agent_outputs)
        self.assertIn("item_0", result)
        self.assertIn("item_1", result)
        
    def test_summary_strategy(self):
        self.compositor.set_strategy(SummaryStrategy())
        result = self.compositor.weave(self.agent_outputs)
        self.assertIn("combined_data", result)
        self.assertEqual(len(result["combined_data"]), 2)

if __name__ == '__main__':
    unittest.main()
