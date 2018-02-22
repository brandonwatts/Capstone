from Api.Models.General.GeneralAPISchema import GeneralAPISchema


class GeneralAPI:

    def __init__(self, nlp_reponse):
        self.nlp_response = nlp_reponse
        self.schema = GeneralAPISchema()

    def mapattrs(self):
        attrs = {}
        if 'state' in self.nlp_response : attrs['State'] = self.nlp_response['state']
        if 'city' in self.nlp_response : attrs['City'] = self.nlp_response['city']
        if 'zip_code' in self.nlp_response : attrs['Zip_Code'] = self.nlp_response['zip_code']
        if 'min_sqft' in self.nlp_response: attrs['Min_Sqft'] = self.nlp_response.get('min_sqft')
        if 'max_sqft' in self.nlp_response : attrs['Max_Sqft'] = self.nlp_response['max_sqft']
        if 'max_price' in self.nlp_response : attrs['Max_Price'] = self.nlp_response['max_price']
        if 'min_bed' in self.nlp_response : attrs['Min_Bed'] = self.nlp_response['min_bed']
        if 'max_bed' in self.nlp_response : attrs['Max_Bed'] = self.nlp_response['max_bed']
        if 'min_price' in self.nlp_response : attrs['Min_Price'] = self.nlp_response['min_price']
        if 'pricing_type' in self.nlp_response : attrs['Pricing_Type'] = self.nlp_response['pricing_type']
        if 'build_year' in self.nlp_response : attrs['Build_Year'] = self.nlp_response['build_year']
        if 'dog_friendly' in self.nlp_response : attrs['Dog_Friendly'] = self.nlp_response['dog_friendly']
        if 'cat_friendly' in self.nlp_response : attrs['Cat_Friendly'] = self.nlp_response['cat_friendly']
        if 'has_pool' in self.nlp_response : attrs['Has_Pool'] = self.nlp_response['has_pool']
        if 'has_elevator' in self.nlp_response : attrs['Has_Elevator'] = self.nlp_response['has_elevator']
        if 'has_finess_center' in self.nlp_response : attrs['Has_Fitness_Center'] = self.nlp_response['has_fitness_center']
        if 'has_wheelchair_access' in self.nlp_response : attrs['Has_Wheelchair_Access'] = self.nlp_response['has_wheelchair_access']
        if 'has_dishwasher' in self.nlp_response : attrs['Has_Dishwasher'] = self.nlp_response['has_dishwasher']
        if 'has_air_conditioning' in self.nlp_response : attrs['Has_Air_Conditioning'] = self.nlp_response['has_air_conditioning']
        if 'has_parking' in self.nlp_response : attrs['Has_Parking'] = self.nlp_response['has_parking']
        if 'has_star_rating' in self.nlp_response : attrs['Star_Rating'] = self.nlp_response.get('star_rating')
        if 'is_furnished' in self.nlp_response : attrs['Furnished'] = self.nlp_response['is_furnished']
        if 'has_laundry_facilities' in self.nlp_response : attrs['Has_Laundry_Facilities'] = self.nlp_response['has_laundry_facilities']
        if 'property_type' in self.nlp_response : attrs['Property_Type'] = self.nlp_response['property_type']

        return attrs

    def call(self):
        api = self.mapattrs()
        response = self.schema.dump(api)
        return response
