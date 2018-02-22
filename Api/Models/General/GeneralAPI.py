from Api.Models.General.GeneralAPISchema import GeneralAPISchema


class GeneralAPI:

    def __init__(self, nlp_reponse):
        self.nlp_response = nlp_reponse
        self.schema = GeneralAPISchema()

    def mapattrs(self):
        attrs = {}
        attrs['State'] = self.nlp_response['state']
        attrs['City'] = self.nlp_response['city']
        attrs['Zip_Code'] = self.nlp_response['zip_code']
        attrs['Min_Sqft'] = self.nlp_response['min_sqft']
        attrs['Max_Sqft'] = self.nlp_response['max_sqft']
        attrs['Min_Price'] = self.nlp_response['min_price']
        attrs['Min_Bed'] = self.nlp_response['min_bed']
        attrs['Max_Bed'] = self.nlp_response['max_bed']
        attrs['Min_Price'] = self.nlp_response['min_price']
        attrs['Pricing_Type'] = self.nlp_response['pricing_type']
        attrs['Build_Year'] = self.nlp_response['build_year']
        attrs['Dog_Friendly'] = self.nlp_response['dog_friendly']
        attrs['Cat_Friendly'] = self.nlp_response['cat_friendly']
        attrs['Has_Pool'] = self.nlp_response['has_pool']
        attrs['Has_Elevator'] = self.nlp_response['has_elevator']
        attrs['Has_Fitness_Center'] = self.nlp_response['has_fitness_center']
        attrs['Has_Wheelchair_Access'] = self.nlp_response['has_wheelchair_access']
        attrs['Has_Dishwasher'] = self.nlp_response['has_dishwasher']
        attrs['Has_Air_Conditioning'] = self.nlp_response['has_air_conditioning']
        attrs['Has_Parking'] = self.nlp_response['has_parking']
        attrs['Star_Rating'] = self.nlp_response.get('star_rating', ["5", "4", "3", "2", "1"])
        attrs['Furnished'] = self.nlp_response['is_furnished']
        attrs['Has_Laundry_Facilities'] = self.nlp_response['has_laundry_facilities']
        attrs['Property_Type'] = self.nlp_response['property_type']

        return attrs

    def call(self):
        api = self.mapattrs()
        response = self.schema.dump(api)
        return response
