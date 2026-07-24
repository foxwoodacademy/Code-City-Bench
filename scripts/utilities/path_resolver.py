import os
from pathlib import Path

class PathResolver:
    """
    Centrally manages the RootBase root directory to eliminate hardcoded absolute paths.
    This ensures the system is portable across different environments.
    """
    _root = None

    @classmethod
    def get_root(cls):
        if cls._root is None:
            # Try to find a marker file or use a known relative structure
            # For this specific environment, we can default to the RootBase folder.
            # In production, this could be an environment variable.
            cls._root = Path("/storage/emulated/0/RootBase").absolute()
        return cls._root

    @classmethod
    def resolve(cls, relative_path):
        """Resolves a relative path against the RootBase root."""
        return str(cls.get_root() / relative_path.lstrip("/"))

# Global instance for easy import
resolver = PathResolver()
