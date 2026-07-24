class Transformer:
    """
    Responsible for modifying data according to transformation rules.
    """

    def __init__(self, transformations):
        """
        Initialize the transformer with a list of transformation rules.

        :param transformations: A list of dictionaries, each describing a transformation.
        """
        self.transformations = transformations

    def transform(self, data):
        """
        Applies transformations to the provided data.

        :param data: The dictionary of data to transform.
        :return: A new dictionary with transformations applied.
        :raises TransformationError: If a transformation fails.
        """
        from .exceptions import TransformationError
        
        # Work on a copy to avoid mutating the original data
        new_data = data.copy()

        for trans in self.transformations:
            action = trans.get('action')

            if action == 'rename':
                self._rename(new_data, trans)
            else:
                # If we encounter an unknown action, we just skip it or could raise an error
                pass

        return new_data

    def _rename(self, data, trans):
        from .exceptions import TransformationError
        
        from_field = trans.get('from')
        to_field = trans.get('to')

        if not from_field or not to_field:
            raise TransformationError("Rename transformation must specify both 'from' and 'to' fields.")

        if from_field in data:
            data[to_field] = data.pop(from_field)
        # Note: If the field is not in the data, we just skip it (it might be optional)
