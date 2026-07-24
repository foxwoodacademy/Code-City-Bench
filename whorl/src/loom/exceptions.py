class LoomError(Exception):
    """Base class for all Loom exceptions."""
    pass

class CompositionError(LoomError):
    """Raised when the composition process fails."""
    pass
