from Api.Models.Apartments.ApartmentsApiSchema import ApiSchema
import json
from Api.Models.Apartments.SearchEndpoint import SearchEndpoint
from Api.Models.Apartments.InfoEndpoint import InfoEndpoint


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
    1: 1,
    2: 2,
    3: 4,
    4: 8,
    5: 16
}


class ApartmentsAPI:

    def __init__(self, nlp_reponse):
        self.nlp_response = nlp_reponse
        self.schema = ApiSchema()
        self.search_endpoint = SearchEndpoint()
        self.info_endpoint = InfoEndpoint()

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
                amenity_code += amenity_codes[amenity_nlp_format_to_apartments_format[i]]
        return amenity_code
    
    def map_ratings(self):
        rating_code = 0
        if "star_rating" in self.nlp_response:
            for i in self.nlp_response["star_rating"]:
                rating_number = [int(s) for s in i.split() if s.isdigit()]
                rating_code += rating_codes[rating_number[0]]
        return rating_code
    
    def mapattrs(self):
        """ Maps the result returned by NLP.py into the correct API Schema designated by CoStar """

        attrs = {}

        attrs['Geography'] = self.ApartmentsAPIObjects.Geography(city=self.nlp_response.get('city'),
                                                                 state=self.nlp_response.get('state'), geotype=2)

        attrs['Listing'] = self.ApartmentsAPIObjects.Listing(ratings=self.map_ratings(),
                                                             min_price=self.nlp_response.get('min_price'),
                                                             max_price=self.nlp_response.get('max_price'),
                                                             min_sqft=self.nlp_response.get('min_sqft'),
                                                             max_sqft=self.nlp_response.get('max_sqft'),
                                                             amenities=self.map_amenities()
                                                             )
        return attrs

    # pulls data from the search enpoint and then the info endpoint
    def call(self):
        Apartments_API = self.create()
        Apartment_IDS, Search_Criteria = self.search_endpoint.call(Apartments_API)
        listings = self.info_endpoint.call(Apartment_IDS, Search_Criteria)
        return listings

    # formats the query for the search endpoint
    def create(self):
        api = self.mapattrs()
        response = self.schema.dump(api)
        return json.dumps(response.data)
