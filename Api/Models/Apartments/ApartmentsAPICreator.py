from Api.Models.Apartments.ApartmentsApiSchema import ApiSchema


class ApartmentsAPICreator:

    def __init__(self, nlp_reponse):
        self.nlp_response = nlp_reponse
        self.schema = ApiSchema()

    class ApartmentsAPIObjects:

        class Geography(object):

            class Address(object):
                def __init__(self, city, state):
                    self.City = city
                    self.State = state

            def __init__(self, geotype, city, state):
                self.GeographyType = geotype
                self.Address = self.Address(city, state)

        class Listing(object):
            def __init__(self, ratings):
                self.Ratings = ratings

    def mapattrs(self):
        attrs = {}
        attrs['Geography'] = self.ApartmentsAPIObjects.Geography(city=self.nlp_response['city'],
                                                                 state=self.nlp_response['state'], geotype=2)
        attrs['Listings'] = self.ApartmentsAPIObjects.Listing(ratings=16)
        return attrs

    def create(self):
        api = self.mapattrs()
        response = self.schema.dump(api)
        return response
