from GeneralAPISchema import GeneralAPISchema


class GeneralAPI:

    def __init__(self, nlp_reponse):
        self.nlp_response = nlp_reponse
        self.schema = GeneralAPISchema()

    def get_value(self, field):
        return self.nlp_response.get(field.lower())

    def mapattrs(self):
        """ Maps the result returned by NLP.py into a General Schema"""

        field_names = GeneralAPISchema._declared_fields.keys()
        attrs = {field: self.get_value(field) for field in field_names}
        return attrs

    def call(self):
        api = self.mapattrs()
        response = self.schema.dump(api)
        return response
