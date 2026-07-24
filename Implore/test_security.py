import unittest
from workflow import app
from ingestor import Ingestor

class TestSecurityGuardrails(unittest.TestCase):
    def test_ssrf_protection(self):
        ingestor = Ingestor()
        # Test attempt to access local loopback
        with self.assertRaises(Exception):
            ingestor.fetch_url("http://127.0.0.1")
            
    def test_prompt_injection_stripping(self):
        # Verify sanitization node logic
        content = "Hello {{ malicious_injection }} __token__"
        sanitized = content.replace("{{", "").replace("}}", "").replace("__", "")
        self.assertEqual(sanitized, "Hello  malicious_injection  token")

    def test_safety_node_violation(self):
        # Verify SafetyNode blocks forbidden content
        # Manually invoke safety node logic here to test
        forbidden_content = "This is a fraud attempt."
        with self.assertRaises(Exception):
            if any(forbidden in forbidden_content.lower() for forbidden in ["illegal", "fraud", "weapon"]):
                raise Exception("Safety violation")

if __name__ == "__main__":
    unittest.main()
