from Api.Models.Apartments.ApartmentsApiSchema import ApiSchema
import json
import requests
import re

pattern = re.compile("(^[a-z0-9]*(?=|))|((?<=[0-9]~)[a-z0-9]*(?=|))")

class ApartmentsAPI:

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
            def __init__(self, ratings, min_price, max_price, min_sqft, max_sqft):
                self.Ratings = ratings
                if min_price:
                    self.MinRentAmount = min_price
                if max_price:
                    self.MaxRentAmount = max_price
                if min_sqft:
                    self.MinSqft = min_sqft
                if max_sqft:
                    self.MaxSqft = max_sqft

    def mapattrs(self):
        attrs = {}
        attrs['Geography'] = self.ApartmentsAPIObjects.Geography(city=self.nlp_response['city'],
                                                                 state=self.nlp_response['state'], geotype=2)
        attrs['Listing'] = self.ApartmentsAPIObjects.Listing(ratings=16, min_price=self.nlp_response.get('min_price'))
        return attrs

    def call(self):
        Apartments_API = self.create()
        Apartment_IDS, Search_Criteria = self.callSearchEndpointWith(Apartments_API)
        return self.callInfoEndpointWith(Apartment_IDS, Search_Criteria)

    def create(self):
        api = self.mapattrs()
        response = self.schema.dump(api)
        print(response)
        return response

    def callSearchEndpointWith(self, data):
        data = json.dumps(data.data)
        headers = {'Content-Type': 'application/json'}
        result = requests.post("https://www.apartments.com/services/search/", data=data, headers=headers)
        search_criteria = json.loads(result.text)["SearchCriteria"]
        result = self.cleanResult(result)
        return result, search_criteria

    def cleanResult(self, result):
        result = json.loads(result.text)
        cl = result['PinsState']['cl']
        ids = re.findall(pattern, cl)
        ids_list = [ids[0][0]] + [id[1] for id in ids[1:]]
        return ids_list


    def callInfoEndpointWith(self, apartment_keys, search_criteria):
        apartment_results = {}
        apartments = []
        for key in apartment_keys:

            call = {}
            call['ListingKeys'] = [str(key)]
            call['SearchCriteria'] = search_criteria
            data = json.dumps(call)
            headers = {'Content-Type': 'application/json'}
            result = requests.post("https://www.apartments.com/services/property/infoCardData", data=data, headers=headers)
            apartment_instance = json.loads(result.text)
            apartments.append(apartment_instance)

        apartment_results['apartments'] = apartments
        return apartment_results