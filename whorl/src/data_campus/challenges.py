import random

class Challenges:
    @staticmethod
    def json_parsing():
        """Challenge 1: Parse a complex JSON structure."""
        return random.choice([True, False, False]) # 33% success

    @staticmethod
    def directory_mapping():
        """Challenge 2: Map a simulated directory structure."""
        return random.choice([True, True, False]) # 66% success

    @staticmethod
    def system_error_resolution():
        """Challenge 3: Resolve a mock system error."""
        return random.choice([True, False]) # 50% success
