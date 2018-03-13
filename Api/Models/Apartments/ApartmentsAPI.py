from Api.Models.Apartments.ApartmentsApiSchema import ApiSchema
import asyncio
import json
import requests
import re

pattern = re.compile("(^[a-z0-9]*(?=|))|((?<=[0-9]~)[a-z0-9]*(?=|))")

'''
--- Amenity Codes ---

In Unit Washer and Dryer    2               2^1  
Dishwasher                  4               2^2
Air Conditioning            16              2^4
Furnished                   128             2^7
Fitness Center              256             2^8
Pool                        512             2^9 
Parking                     65536           2^16    
Wheelchair Access           131072          2^17   
Elevator                    524288          2^19             
Washer and Dryer Hookups    1048576         2^20
Laundry Facilities          2097152         2^21
Utilities Included          4194304         2^22  
Lofts                       8388608         2^23

Dog Friendly                Not an amenity (PetFriendly: 1)
Cat Friendly                Not an amenity (PetFriendly: 2)
'''

amenity_nlp_format_to_apartments_format = {
#   'has_washer_and_dryer'      :   'IN_UNIT_WASHER_AND_DRYER',
    'has_dishwasher'            :   'DISHWASHER',
    'has_air_conditioning'      :   'AIR_CONDITIONING',
    'is_furnished'              :   'FURNISHED',
    'has_fitness_center'        :   'FITNESS_CENTER',
    'has_pool'                  :   'POOL',
    'has_parking'               :   'PARKING',
    'has_wheelchair_access'     :   'WHEELCHAIR_ACCESS',
    'has_elevator'              :   'ELEVATOR',
    'has_laundry_facilities'    :   'LAUNDRY_FACILITIES'#,
#   'has_utilities_included'    :   'UTILITIES_INCLUDED'#,
#   'is_loft'                   :   'LOFTS'
}

amenity_codes = {
    'IN_UNIT_WASHER_AND_DRYER'  : 2,
    'DISHWASHER' 				: 4,
    'AIR_CONDITIONING' 			: 16,
    'FURNISHED'					: 128,
    'FITNESS_CENTER' 			: 256,
    'POOL'						: 512,
    'PARKING'					: 65536,
    'WHEELCHAIR_ACCESS'			: 131072,
    'ELEVATOR'					: 524288,
    'WASHER_AND_DRYER_HOOKUPS'	: 1048576,
    'LAUNDRY_FACILITIES'		: 2097152,
    'UTILITIES_INCLUDED'		: 4194304,
    'LOFTS'						: 8388608
}

'''
--- Star Rating Codes

5 Star 16
4 Star 8
3 Star 4
2 Star 2
1 Star 1
'''

rating_codes = {
    1 : 1,
    2 : 2,
    3 : 4,
    4 : 8,
    5 : 16
}

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
            def __init__(self, ratings, min_price, max_price, min_sqft, max_sqft, amenities):
                self.Ratings = ratings
                if min_price:
                    self.MinRentAmount = min_price
                if max_price:
                    self.MaxRentAmount = max_price
                if min_sqft:
                    self.MinSqft = min_sqft
                if max_sqft:
                    self.MaxSqft = max_sqft
                if amenities:
                    self.Amenities = amenities

    # Maps all the amenity filters our nlp_response tells us to use to the encoding for apartments.com
    def map_amenities(self):
        amenity_code = 0
        for i in self.nlp_response:
            if i in amenity_nlp_format_to_apartments_format:
                amenity_code += amenity_codes[i]
        return amenity_code
    
    def map_ratings(self):
        rating_code = 0
        if "star_rating" in self.nlp_response:
            for i in self.nlp_response["star_rating"]:
                rating_code += rating_codes[i]
        return rating_code
    
    # converts the nlp_response into the schema format 
    def mapattrs(self):
        attrs = {}
        attrs['Geography'] = self.ApartmentsAPIObjects.Geography(city=self.nlp_response['city'],
                                                                 state=self.nlp_response['state'], geotype=2)
        attrs['Listing'] = self.ApartmentsAPIObjects.Listing(ratings=self.map_ratings(),
                                                             min_price=self.nlp_response.get('min_price'),
                                                             max_price=self.nlp_response.get('max_price'),
                                                             min_sqft=self.nlp_response.get('min_sqft'),
                                                             max_sqft=self.nlp_response.get('max_sqft'),
                                                             amenities=self.map_amenities())
        return attrs

    # pulls data from the search enpoint and then the info endpoint
    def call(self):
        Apartments_API = self.create()
        Apartment_IDS, Search_Criteria = self.callSearchEndpointWith(Apartments_API)
        return self.callInfoEndpointWithAll(Apartment_IDS, Search_Criteria)

    # formats the query for the search endpoint
    def create(self):
        api = self.mapattrs()
        response = self.schema.dump(api)
        print(response)
        return response

    # returns the unextracted keys and search criteria from the search endpoint
    def callSearchEndpointWith(self, data):
        data = json.dumps(data)
        headers = {'Content-Type': 'application/json'}
        result = requests.post("https://www.apartments.com/services/search/", data=data, headers=headers)
        search_criteria = json.loads(result.text)["SearchCriteria"]
        result = self.cleanResult(result)
        return result, search_criteria

    # returns the keys from the search endpoint
    def cleanResult(self, result):
        result = json.loads(result.text)
        cl = result['PinsState']['cl']
        ids = re.findall(pattern, cl)
        ids_list = [ids[0][0]] + [id[1] for id in ids[1:]]
        return ids_list

    async def callInfoEndpointWith(self, key, search_criteria):
        url = "https://www.apartments.com/services/property/infoCardData"
        call = {'ListingKeys': [str(key)], 'SearchCriteria': search_criteria}
        data = json.dumps(call)
        headers = {'Content-Type': 'application/json'}
        
        loop = asyncio.get_event_loop()
        future = loop.run_in_executor(None, lambda: requests.post(url, data, headers=headers))
        
        result = await future
        return json.loads(result.text)
    
    # returns property information of the given keys
    def callInfoEndpointWithAll(self, apartment_keys, search_criteria):
        loop = asyncio.get_event_loop()
        apartments = loop.run_until_complete(
            asyncio.gather(*[self.callInfoEndpointWith(key, search_criteria)
                             for key in apartment_keys]))
        return {'apartments': apartments}
