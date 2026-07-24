import json
from .validator import Validator
from .transformer import Transformer
from .exceptions import ManifestError, ValidationError, TransformationError

class DataWeaver:
    """
    The main interface for the DataWeaver module.
    Coordinates validation and transformation of data based on a manifest.
    """

    def __init__(self, manifest_path):
        """
        Initialize DataWeaver with a manifest file.

        :param manifest_path: Path to the manifest.json file.
        """
        self.manifest = self._load_manifest(manifest_path)
        self.validator = Validator(self.manifest.get('schema', {}))
        self.transformer = Transformer(self.manifest.get('transformations', []))

    def _load_manifest(self, path):
        try:
            with open(path, 'r') as f:
                manifest = json.load(f)
            
            # Basic manifest validation
            if 'metadata' not in manifest:
                raise ManifestError("Manifest is missing required 'metadata' section.")
            if 'schema' not in manifest:
                raise ManifestError("Manifest is missing required 'schema' section.")
                
            return manifest
        except FileNotFoundError:
            raise ManifestError(f"Manifest file not found at: {path}")
        except json.JSONDecodeError:
            raise ManifestError(f"Manifest file is not valid JSON: {path}")
        except Exception as e:
            raise ManifestError(f"An error occurred while loading the manifest: {str(e)}")

    def process(self, data):
        """
        Validates and then transforms the provided data.

        :param data: The dictionary of data to process.
        :return: The transformed data dictionary.
        :raises ValidationError: If validation fails.
        :raises TransformationError: If transformation fails.
        """
        # 1. Validate
        self.validator.validate(data)
        
        # 2. Transform
        processed_data = self.transformer.transform(data)
        
        return processed_data
