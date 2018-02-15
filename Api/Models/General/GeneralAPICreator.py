from Api.Models.General import GeneralAPISchema


class GeneralAPICreator:

    def __init__(self, nlp_reponse):
        self.nlp_response = nlp_reponse
        self.schema = GeneralAPISchema()


    def mapattrs(self):
        attrs = {}
        attrs['State'] = self.nlp_response['state']
        attrs['City'] = self.nlp_response['city']
        return attrs

    def create(self):
        api = self.mapattrs()
        response = self.schema.dump(api)
        return response
