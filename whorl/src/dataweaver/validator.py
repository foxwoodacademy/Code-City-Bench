import re

class Validator:
    """
    Responsible for checking if a data dictionary adheres to a provided schema.
    """

    def __init__(self, schema):
        """
        Initialize the validator with a schema.
        
        :param schema: A dictionary representing the schema rules.
        """
        self.schema = schema

    def validate(self, data):
        """
        Validates the provided data against the schema.

        :param data: The dictionary of data to validate.
        :raises ValidationError: If the data does not conform to the schema.
        """
        for field, rules in self.schema.items():
            # Check for required fields
            if rules.get('required', False) and field not in data:
                from .exceptions import ValidationError
                raise ValidationError(f"Missing required field: '{field}'")

            if field in data:
                value = data[field]
                expected_type_name = rules.get('type')

                # Check type
                self._check_type(field, value, expected_type_name)

                # Check numeric constraints
                if expected_type_name == 'number':
                    self._check_numeric_constraints(field, value, rules)

                # Check string pattern
                if expected_type_name == 'string' and 'pattern' in rules:
                    self._check_pattern(field, value, rules['pattern'])

    def _check_type(self, field, value, expected_type_name):
        from .exceptions import ValidationError
        
        type_map = {
            'string': str,
            'number': (int, float),
            'boolean': bool,
            'object': dict,
            'array': list
        }

        if expected_type_name not in type_map:
            # If the type in schema is unknown, we'll just skip it for now or could raise an error
            return

        if not isinstance(value, type_map[expected_type_name]):
            raise ValidationError(
                f"Field '{field}' must be of type {expected_type_name}, but got {type(value).__name__}"
            )

    def _check_numeric_constraints(self, field, value, rules):
        from .exceptions import ValidationError
        
        if 'min' in rules and value < rules['min']:
            raise ValidationError(f"Field '{field}' is too small. Minimum value is {rules['min']}, but got {value}")
        
        if 'max' in rules and value > rules['max']:
            raise ValidationError(f"Field '{field}' is too large. Maximum value is {rules['max']}, but got {value}")

    def _check_pattern(self, field, value, pattern):
        from .exceptions import ValidationError
        
        if not re.match(pattern, value):
            raise ValidationError(f"Field '{field}' does not match the required pattern: {pattern}")
