class DataWeaver:
    """
    Connects FEP runtime field states to Implore grant data or other external signals.
    """
    def weave(self, field_state, external_signal):
        """Maps physical field state to informational signal."""
        # This is where we link FEP state to grant opportunity strength
        return {"woven_signal": sum(map(sum, field_state)) * external_signal}
