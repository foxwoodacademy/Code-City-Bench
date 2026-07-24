# DataWeaver Technical Reference

This document provides technical details regarding the implementation, architecture, and usage of the DataWeaver module.

## Architecture

DataWeaver follows a modular design to ensure clear separation of concerns:

- **`DataWeaver` (Core Engine)**: The primary entry point. It orchestrates the loading of the manifest, the validation process, and the transformation process.
- **`Validator`**: Responsible for enforcing the `schema` defined in the manifest. It handles type checking, required field checks, numeric range checks, and regex pattern matching.
- **`Transformer`**: Responsible for applying the `transformations` defined in the manifest to the validated data.
- **`Exceptions`**: Provides a hierarchy of custom exceptions for precise error handling.

## Manifest Specification (`manifest.json`)

The `manifest.json` is the configuration file that defines the rules.

### Schema Constraints

| Constraint | Type | Description |
| :--- | :--- | :--- |
| `type` | `string` | `string`, `number`, `boolean`, `object`, `array` |
| `required` | `boolean` | If `true`, the field must exist. |
| `min` | `number` | Minimum value for `number` types. |
| `max` | `number` | Maximum value for `number` types. |
| `pattern` | `string` | Regex pattern for `string` types. |

### Transformation Actions

Currently supported actions:

- `rename`: Changes a field name from `from` to `to`.

## API Usage

### Basic Usage

```python
from dataweaver.core import DataWeaver

# Initialize with manifest path
dw = DataWeaver("path/to/manifest.json")

# Process data
try:
    input_data = {"temp": 22, "sensor_id": "ABC"}
    clean_data = dw.process(input_data)
    print(clean_data)
except Exception as e:
    print(f"Error: {e}")
```

## Error Handling

DataWeaver raises the following exceptions:

- `ManifestError`: Raised during initialization if the manifest is missing, invalid JSON, or lacks required sections.
- `ValidationError`: Raised during `.process()` if the data violates the schema.
- `TransformationError`: Raised during `.process()` if a transformation step fails.
