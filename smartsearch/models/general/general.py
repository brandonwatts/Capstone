from smartsearch.models.general.general_schema import GeneralSchema

class SchemaError(Exception):
    def __init__(self, message):
        super().__init__(message)

_schema = GeneralSchema()

def _mapattrs(attributes):
    """ Maps the result returned by nlp.py into a General Schema"""
    
    field_names = GeneralSchema._declared_fields.keys()
    
    if any(field not in field_names for field in attributes):
        fields = [field for field in attributes if field not in field_names]
        raise SchemaError("fields not in the schema given: {}" % str(fields))
    
    return {field: attributes.get(field) for field in field_names}

def call(attributes):
    return _schema.dump(_mapattrs(attributes))
