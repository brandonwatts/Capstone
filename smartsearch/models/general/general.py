from smartsearch.models.general.general_schema import GeneralSchema

class SchemaError(Exception):
    pass

_schema = GeneralSchema()

def _mapattrs(attributes):
    """ Maps the result returned by nlp.py into a General Schema"""
    
    field_names = GeneralSchema._declared_fields.keys()
    
    if any(field not in field_names for field in attributes):
        for field in attributes:
            if field not in field_names:
                print(field)
                print("OOOOOH FUCkl")
        raise SchemaError()
    
    return {field: attributes.get(field) for field in field_names}

def call(attributes):
    return _schema.dump(_mapattrs(attributes))
