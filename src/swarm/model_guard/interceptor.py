import logging

# Define threshold for "competence" (minimum parameter count)
COMPETENCE_THRESHOLD_BILLIONS = 7.0 

class ModelGuard:
    def __init__(self):
        self.logger = logging.getLogger("ModelGuard")

    def inspect(self, model_name, param_size_b):
        """Intercepts model call and validates against thresholds."""
        if param_size_b < COMPETENCE_THRESHOLD_BILLIONS:
            self.logger.warning(f"[!!!] SAFETY INTERCEPT: Model {model_name} ({param_size_b}B) is too weak for production code.")
            return False
        return True
