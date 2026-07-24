class DataWeaverError(Exception):
    """Base class for all DataWeaver exceptions."""
    pass

class ManifestError(DataWeaverError):
    """Raised when the manifest itself is invalid."""
    pass

class ValidationError(DataWeaverError):
    """Raised when the data fails to meet the schema requirements."""
    pass

class TransformationError(DataWeaverError):
    """Raised when a transformation fails."""
    pass
